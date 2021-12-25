from bs4 import BeautifulSoup
from sty import bg, fg, rs, Style, RgbBg, RgbFg, ef
import requests
import os, time, textwrap


def show_blog(url: str):

    # while until we get html code of given url
    while True:
        os.system("clear")
        print("Blog yükleniyor...")

        try:
            URL = url
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            break  # getting html code is ok (break runs if no error occured until now)

        except Exception as e:
            os.system("clear")
            while True:
                restart = False

                print(
                    f"Blog verisi alınamadı.\nTekrar denemek için {ef.b}t{ef.rs} giriniz.\nÇıkmak için {ef.b}Ctrl+C{ef.rs}'ye basınız ya da {ef.b}q{ef.rs} giriniz.\nHata metni için {ef.b}e{ef.rs} giriniz."
                )
                inpt = input()
                if inpt.lower() == "e":
                    print("---")
                    print(e)
                    print("---")
                elif inpt.lower() == "t":
                    restart = True
                    break
                elif inpt.lower().strip() in ["", "q"]:
                    return 0
                else:
                    print("Geçersiz komut")

            if not restart:
                break

    os.system("clear")

    print(
        ef.bold
        + soup.find("h2", class_="qodef-post-title").text.strip()
        + "\nYazar: "
        + ef.rs
        + soup.find("a", class_="qodef-post-info-author-link").text
        + "\n"
    )  # print author

    # get the parent div which we need to work on
    # this div contains blog post's text(content) that we need to print
    parent = soup.find("div", "qodef-post-text-inner")

    # find header elements
    headers = [header.text for header in parent.find_all("h3")]

    # find list elements
    list_elements = [li.text for li in parent.find_all("li")]

    # find style elements
    style_texts = [style.text for style in parent.find_all("style")]

    # after we detected our unwanted elements, we can get all text(innerHTML) of elements
    blog_text = parent.text

    # delete style element's innerHTML from our text
    for s in style_texts:
        blog_text = blog_text.replace(s, "")

    # convert our multi-line string to array
    blog_text = blog_text.splitlines()

    # Now blog_text contains: date, title, author, category and blog post's text

    # get rid of datas before blog post's text
    # category is the last unwanted element, so just cutting array from there
    last_unwanted = soup.find("div", class_="qodef-post-info-category").text.strip()
    for index, value in enumerate(blog_text):
        if last_unwanted in value.strip():
            blog_text = blog_text[index + 1 :]
            break

    # delete empty elements
    blog_text = [
        line.replace("\xa0", "")
        for line in blog_text
        if len(line) > 0 and not line == "\xa0"
    ]

    terminal_width = os.get_terminal_size()[0]  # to fit the text inside terminal
    padding_right = 3

    # print the blog text
    for line in blog_text:
        if line in headers:
            # recognized header
            print(f"\n{ef.bold}{line}{ef.rs}")

        elif line in list_elements:
            # recognized list element
            print(f"◦ {line}")

        else:
            print(textwrap.fill(line, terminal_width - padding_right))

    print(f"---\nLink: {fg.li_blue}{url}{fg.rs}\n")
    input("Menüye dönmek için enter tuşuna basınız.")


def menu():

    fg.title_fg = Style(RgbFg(255, 255, 255))
    bg.title_bg = Style(RgbBg(83, 83, 99))
    fg.link_fg = Style(RgbFg(6, 69, 173))

    page_index = 0

    while True:
        os.system("clear")
        print("Yükleniyor...")

        # page shouldn't be lower than zero
        page_index = page_index if page_index >= 0 else 0

        try:
            URL = "https://www.artistanbul.io/blog/page/" + str((page_index // 2) + 1)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
        except Exception as e:
            os.system("clear")
            while True:
                restart = False

                print(
                    f"Veri alınamadı.\nTekrar denemek için {ef.b}t{ef.rs} giriniz.\nÇıkmak için {ef.b}Ctrl+C{ef.rs}'ye basınız ya da {ef.b}q{ef.rs} giriniz.\nHata metni için {ef.b}e{ef.rs} giriniz."
                )

                inpt = input()
                if inpt.lower() == "e":
                    print("---")
                    print(e)
                    print("---")
                elif inpt.lower() == "t":
                    restart = True
                    break
                elif inpt.lower().strip() in ["", "q"]:
                    return 0
                else:
                    print("Geçersiz komut")

            if restart:
                continue

        # collect datas to display about blogs
        titles = soup.find_all("h2", class_="qodef-post-title")
        authors = soup.find_all("a", class_="qodef-post-info-author-link")
        dates = soup.find_all("span", class_="date")
        months = soup.find_all("span", class_="month")

        os.system("clear")

        url = [None] * 5

        """
        We get 10 blogs with one request but I split them to half for better UX
        exmpl: page_index 0 and 1 send request to page 1 (page_index=0 displays first 5 blogs, 1 displays other 5 blogs on page 1)
            page_index 2 and 3 send request to page 2 (page_index=2 displays first 5 blogs, 3 displays other 5 blogs on page 2)
        """
        for index, title in enumerate(
            titles[5 * (page_index % 2) : 5 * (page_index % 2) + 5]
        ):
            print(
                fg.green
                + ef.b
                + str(index + 1)
                + ")"
                + ef.i
                + bg.title_bg
                + fg.title_fg
                + " "
                + title.find("a").text
                + "  "
                + fg.rs
                + bg.rs
                + ef.rs
            )  # print title of blog post
            print(
                f"({dates[index + ((page_index%2)*5)].text} {months[index + ((page_index%2)*5)].text}) {ef.bold}Yazar:{ef.rs} {authors[index + ((page_index%2)*5)].text}"
            )  # print date and author
            print()
            url[index] = title.find("a")["href"]  # store link of blog post

            time.sleep(0.1)  # for animation

        print(f"Sayfa {page_index+1}\n")  # page indicator

        # ask user for command
        reply = str(
            input(
                f"Komutlar: ileri, geri, <blog numarası ({ef.b + fg.green}1{ef.rs + fg.rs}-{ef.b + fg.green}5{ef.rs + fg.rs})>, yardım\n-> "
            )
        )

        # handle unknown commands
        expected_commands = ["ileri", "geri", "q", "1", "2", "3", "4", "5"]
        while not reply in expected_commands:
            reply = str(
                input(
                    f"---\nÇıkmak için {ef.i}ctrl+c{ef.rs}'ye basınız ya da {ef.bold}q{ef.rs} giriniz.\nOkumak için {ef.b + fg.green}1{ef.rs + fg.rs}-{ef.b + fg.green}5{ef.rs + fg.rs} arasında numara giriniz\nSonraki sayfa için '{ef.b}ileri{ef.rs}' yazınız\nÖnceki sayfa için '{ef.b}geri{ef.rs}' yazınız\n-> "
                )
            )

        # act for commands
        if reply.lower() == "ileri":
            page_index += 1
        elif reply.lower() == "geri":
            page_index -= 1
        elif reply.isdigit():
            show_blog(url[int(reply) - 1])
        elif reply == "q":
            return 0


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        # passes traceback
        print("\nÇıkış yaptınız.")
    except Exception as e:
        # ask user for showing error text
        inp = input(
            f"Hata! Hata metnini görmek için {ef.bold}e{ef.rs} giriniz.\nKapatmak için enter'a basınız.\n"
        )
        if inp.lower().strip() == "e":
            print(e)
