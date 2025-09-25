from bs4 import BeautifulSoup
import pypandoc
import os
import urllib
import ssl
import sys
import shutil
import tempfile


# Set the pandoc path if running from a PyInstaller (compiled) executable
if getattr(sys, 'frozen', False):
    pandoc_path = os.path.join(sys._MEIPASS, "pypandoc", "files")
    pypandoc.pandoc_path = pandoc_path


def download_replace_images(soup):
    if sys.platform == "darwin":
        # Give up verifying certificates
        context = ssl._create_unverified_context()
    else:
        context = ssl.create_default_context()
        context.set_default_verify_paths()

    img_dir = tempfile.mkdtemp()

    count = 0
    for img in soup.find_all("img"):
        img_url = img["src"]
        img_name = f"image{count:03d}.jpg"
        img_path = os.path.join(img_dir, img_name)

        try:
            with urllib.request.urlopen(img_url, context=context) as response:
                with open(img_path, "wb") as file:
                    file.write(response.read())
                img["src"] = img_path  # Update HTML with local image path
                count += 1
        except Exception as e:
            print(f"Failed to download {img_url}\n{e}")
    return img_dir


def remove_image_labels(row):
    image = row.find("img")
    sibling = image.find_next_sibling("div")
    # Go through all "div" sub-elements of the image and remove them
    while sibling:
        next_sibling = sibling.find_next_sibling("div")
        sibling.decompose()
        sibling = next_sibling


def clean_up_title(row):
    link = row.find("a")
    full_title = link.string

    # e.g. of full title : `Le silence : roman / Dennis Lehane ; traduit de l'américain par François Happe.`
    # We only want to keep the actual title, so remove everything after the first `/` (the author part)
    title = full_title.split("/", 1)[0]

    # Write it back in the link
    link.string = title.strip()


def should_keep(row):
    keywords = {"Auteur", "Résumé", "Cote"}
    has_field_of_interest = any(keyword in row.get_text() for keyword in keywords)
    has_title_link = bool(row.find("a"))
    has_image = bool(row.find("img"))
    return has_field_of_interest or has_title_link or has_image


def main(input: str):
    # Load the HTML file
    with open(input, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Remove the "base href" attribute, which messes links
    base = soup.find("base")
    base.decompose()

    # Download and replace all images with the local version
    # Pypandoc (converting to Word) occasionally had issues fetching the images
    img_folder = download_replace_images(soup)

    # Process all tables
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            if should_keep(row):
                # The row contains important stuff - process it further if necessary

                # Remove "author" from title (title is a link, "a")
                if bool(row.find("a")):
                    clean_up_title(row)

                # Clean up images
                if bool(row.find("img")):
                    remove_image_labels(row)
            else:
                row.decompose()

    # Convert to Word document
    output = os.path.splitext(input)[0] + ".docx"
    pypandoc.convert_text(source=str(soup), format="html", to="docx", outputfile=output, extra_args=["-RTS", "--embed-resources", "--standalone"])

    # Remove downloaded images
    if os.path.exists(img_folder):
        shutil.rmtree(img_folder, ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_files = sys.argv[1:]
        for file in input_files:
            if os.path.isfile(file):
                try:
                    main(file)
                except Exception as e:
                    print(f"Erreur lors du traitement du fichier {file} : {e}")
            else:
                print(f"Erreur lors de la lecture du fichier {file}.")
    else:
        print("Utilisation: glissez et déposez un (ou plusieurs) fichiers HTML sur l'exécutable (.exe) pour les filtrer et les convertir en document Word.")
