import os
import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import telebot
from datetime import datetime
from glob import glob
import os
import re


def get_data_from_ijo(n_data):
    global driver

    data = {}
    print("Opening Browser")
    os.environ['PATH'] += os.pathsep + "F:\\Google Drive\\My File\\Belajar Programing\\Python\\emak2ijobot\\webdriver"
    driver = webdriver.Firefox()
    url = 'https://www.tokopedia.com/discovery/kejar-diskon'
    print("Opening Tokopedia Flash Sale")
    driver.get(url)
    print("Trying To Click That Option")
    try:
        barrier = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, r'.unf-coachmark__next-button')))
        barrier.click()
    except Exception as e:
        print("Option Not Found")
        print(e)

    """act = driver.find_element(By.CSS_SELECTOR, r'.css-1656jox').text
    time_act = act.split(" ")[0]
    print(time_act)"""

    all = []
    link_all = []
    n = 0
    while n < n_data:
        print(f"Data Program ({n}) > Data From Website ({n_data})")
        print("Updating Data")
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
        time.sleep(3)
        all = driver.find_element(By.CSS_SELECTOR,
                                  r'div.css-g90k5e:nth-child(5) > div:nth-child(1) > div:nth-child(1)')
        list_all = all.find_elements(By.TAG_NAME, 'a')
        link_all = []
        for li in list_all:
            url = li.get_attribute('href')
            # print(url)
            if url not in link_all:
                link_all.append(url)

        n = len(link_all)
        print(f"Sum Data Afer Scrolling = {n}")

    all = driver.find_element(By.CSS_SELECTOR,
                              r'div.css-g90k5e:nth-child(5) > div:nth-child(1) > div:nth-child(1)')
    list_all = all.find_elements(By.TAG_NAME, 'a')
    link_all = []
    for li in list_all:
        url = li.get_attribute('href')
        # print(url)
        if url not in link_all:
            link_all.append(url)
    print(f"Sum Link = {len(link_all)}")

    for dat in range(len(list_all)):
        raw = list_all[dat].text.split('\n')
        # print(f"data= {list_all[dat].text}, type= {type(list_all[dat].text)}, list = {len(raw)}")
        if len(raw) != 1:
            produk = raw[1].lower()
            harga = raw[2]
            diskon = raw[3]
            kota = raw[4]
            if produk not in data:
                # print(f"{produk} = {harga}, {diskon}, {kota}")
                data[produk] = {"harga": harga, "diskon": diskon, "kota": kota}

    # jogress
    for lo in data:
        ins = link_all[0]
        data[lo]['link'] = ins
        link_all.remove(ins)

    print(f"Sum of Data = {len(data)}")

    driver.quit()
    return data

    # cek = driver.find_element(by=By.CLASS_NAME, value="intersection-visible-wrapper").find_elements()
    """cek = driver.find_element(By.XPATH, r'/html/body/div[1]/div/main/div[1]/div[4]/div/div/div/div[5]/div/div').text
    print(cek)"""
    # cek = driver.find_element_by_class_name('intersection-visible-wrapper')

    # css path = html body div div.css-83xqh5-unf-coachmark.e1o9jid31 section.css-1frsvni-unf-card.eeeacht0 div.unf-coachmark__content-wrapper.css-8atqhb.e1o9jid32 div.unf-coachmark__footer.css-1i5hdkt.e1o9jid34 div.unf-coachmark__action-wrapper.css-1xhj18k.e1o9jid33 div.unf-coachmark__next-button.css-64apm5.e1o9jid35
    # xpath = /html/body/div[5]/div[7]/section/div/div/div[2]/div
    # class = intersection-visible-wrapper
    # time.sleep(30)
    # print("quitt")


def send_message_emakbot(message, id):
    return emakbot.send_message(id, message)


def looop():
    time_check = [8, 10, 12, 14, 16, 18, 20]
    n_kali = 0
    while True:
        time_raw = datetime.now()
        rn = time_raw.strftime('%H')
        #print(rn)
        if int(rn) in time_check and n_kali == 0:
            n_kali = 1
            for ids in get_id():
                emakbot.send_message(ids,"Searching For Promo")
                force_cek(ids)
            emakbot.send_message(ids, "Waiting....")
            time.sleep(1800)
        else:
            time_sekrang = datetime.now().time()
            print(f"Waiting for another time, {time_sekrang}")
            n_kali = 0
            time.sleep(1800)

def thread_loop():
    global loop_thread_n
    if loop_thread_n == 0:
        loop_thread = threading.Thread(target=looop(), daemon=True)
        loop_thread_n = 1
        loop_thread.start()
        loop_thread.join()
    else:
        print("Loop Threading already start ")


def get_id():
    # xxmain_path = os.path.dirname(os.path.realpath(__file__))
    data_path = r"F:\Google Drive\My File\Belajar Programing\Python\emak2ijobot\data" #path to notepad
    # print(f"{main_path}\\data\\")
    file = glob(f"{data_path}\\*.txt")
    file_send = []
    for x in file:
        raw1 = x.split('\\')
        raw2 = raw1[-1].split('.')
        raw = raw2[0]
        if raw not in file_send:
            file_send.append(raw)
    return file_send


def get_kk(id):
    data_path = r"F:\Google Drive\My File\Belajar Programing\Python\emak2ijobot\data" #path to notepad
    try:
        all_list = []
        with open(f"{data_path}\\{id}.txt", 'r') as file:
            all_list = file.read().splitlines()
            return all_list
    except:
        return 0


def force_cek(ids):
    try:
        all_data_ijo = get_data_from_ijo(n_barang)
        ada=[]
        barangsay = get_kk(ids)
        n_match_param = 3

        #print(all_data_ijo)
        for datasay in barangsay:
            for all_sat in all_data_ijo:
                n_ada = 0
                data_split = datasay.split(" ")

                all_data_split = [x.lower() for x in all_sat.split(" ")]

                for sp in data_split:
                    if sp.lower() in all_data_split and sp.isalnum():
                        n_ada += 1

                if n_ada > n_match_param:
                    #print(f"{datasay} = {all_sat}")
                    #print(data_split)
                    #print(all_data_split)
                    print(f"Found {datasay}")
                    print(f"For Product {datasay} match data {n_ada}")
                    barang = all_sat
                    harga = all_data_ijo[all_sat]['harga']
                    diskon = all_data_ijo[all_sat]['diskon']
                    link = all_data_ijo[all_sat]['link']
                    # link=0
                    ada.append(barang)
                    msg = f"{barang}\n{harga}\n{diskon}\n{link}"
                    emakbot.send_message(ids, msg)
                    break

        if len(ada) == 0:
            emakbot.send_message(ids, "There is No Promo")

    except Exception as e:
        print(e)
        msg = "Can't Find any Data"
        print(msg)
        emakbot.send_message(ids, msg)

def telegram_threading():
    tele = threading.Thread(target=telegram, daemon=True)
    tele.start()

def telegram():

    global emakbot
    token = r"5340683319:AAG04A1VPxtGfy0x_3sassxbYgVDAwouPyM" #token
    emakbot = telebot.TeleBot(token)


    @emakbot.message_handler(commands=['start'])
    def start(message):
        msg = f"Start Finding Promo, fill /tambah For me to search any promo that you need"
        print(f"Send Message {msg}")
        emakbot.send_message(message.chat.id, msg)


    @emakbot.message_handler(commands=['help'])
    def help(message):
        msg = f"""
        Write /cek for Checking any promo\nwrite /list_emak to check your list\nwrite /tambah(space)items to add item to your list\nwrite /hapus for delete your items in lists
              """
        print(f"Send Message {msg}")
        emakbot.send_message(message.chat.id, msg)


    @emakbot.message_handler(commands=['jum_data'])
    def jum_data(message):
        global n_barang
        msg = f"Jumlah data yang akan dicari  sekarang sebanyak = {n_barang} akan dirubah menjadi yang kamu mau"
        print(f"Send Message {msg}")
        emakbot.send_message(message.chat.id, msg)
        raw_raw = message.text.split(" ")
        raw_raw.pop(0)
        try:
            jum_new = int(" ".join(raw_raw))
            n_barang = jum_new
            emakbot.send_message(message.chat.id, f"sekarang mencari {n_barang} barang setiap kalinya")
            print(f"barang dicari {n_barang}")
        except Exception as e:
            print(e)
            emakbot.send_message(message.chat.id, f"Tidak bisa membaca jumlah barang")


    @emakbot.message_handler(commands=['tambah'])
    def tambah(message):
        msg = f"Writing your item to list"
        print(f"Send Message {msg}")
        emakbot.send_message(message.chat.id, msg)
        data_path = r"F:\Google Drive\My File\Belajar Programing\Python\emak2ijobot\data"#data path
        data = message.text
        new_msg_raw = data.split(" ")
        new_msg_raw.remove("/tambah")
        new_msg = " ".join(new_msg_raw).lower()
        all_list_data_old = get_kk(message.chat.id)
        if new_msg not in all_list_data_old:
            with open(f"{data_path}\\{message.chat.id}.txt", 'a+') as file:
                file.writelines(f"\n{new_msg}")
        emakbot.send_message(message.chat.id, f"Your new added item {new_msg}")


    @emakbot.message_handler(commands=['list_emak'])
    def list_emak(message):
        msg = f"Your List: "
        print(f"Send Message {msg}")
        emakbot.send_message(message.chat.id, msg)
        list_barang = get_kk(message.chat.id)
        try:
            if "" in list_barang:
                list_barang.remove("")

            data_path = r"F:\Google Drive\My File\Belajar Programing\Python\emak2ijobot\data"
            with open(f"{data_path}\\{message.chat.id}.txt", 'w') as file:
                for li in list_barang:
                    file.write(f"{li}\n")

        except Exception as e:
            print(e)

        n = 1
        print(list_barang)
        if len(list_barang) != 0:
            for barang in list_barang:
                if barang != " ":
                    emakbot.send_message(message.chat.id, f"{n}. {barang}")
                    n += 1

        else:
            emakbot.send_message(message.chat.id, 'Theres no item in your list')


    @emakbot.message_handler(commands=['hapus'])
    def tambah(message):
        msg = f"Deleting Data "
        print(f"Send Message {msg}")
        emakbot.send_message(message.chat.id, msg)
        data_path = r"F:\Google Drive\My File\Belajar Programing\Python\emak2ijobot\data"
        data = message.text
        del_msg_raw = data.split(" ")
        del_msg_raw.remove(r'/hapus')
        del_msg = " ".join(del_msg_raw).lower()
        print(del_msg)
        all_list_data_old = get_kk(message.chat.id)
        print(all_list_data_old)
        try:
            all_list_data_old.remove(del_msg)
        except Exception as e:
            print(e)
            return emakbot.send_message(message.chat.id, "no item in your list")

        with open(f"{data_path}\\{message.chat.id}.txt", 'w') as file:
            for li in all_list_data_old:
                file.write(f"{li}\n")
        emakbot.send_message(message.chat.id, f"items removed")


    @emakbot.message_handler(commands=['cek'])
    def cek(message):
        msg = f"Checking For Promo"
        print(f"Send Message {msg}")
        emakbot.send_message(message.chat.id, msg)
        force_cek(message.chat.id)
        # force cek


    @emakbot.message_handler(commands=['test'])
    def test(message):
        msg = f"testing dengan message id {message.chat.id}"
        print(f"Send Message {msg}")
        emakbot.send_message(message.chat.id, msg)


    @emakbot.message_handler(func=lambda message: True)
    def repeat(message):
        emakbot.reply_to(message, "I don't understand write /help for see available commands")


    print("Starting Program")

    global n_barang, loop_thread_n, force_thread_n

    n_barang = 50
    loop_thread_n = 0
    force_thread_n = 0

    emakbot.polling()

# ois = get_data_from_ijo(50)

"""for oi in ois:
    print(f"{oi} = {ois[oi]}")"""

n_barang = 100
loop_thread_n = 0
force_thread_n = 0

global emakbot
token = r"5340683319:AAG04A1VPxtGfy0x_3sassxbYgVDAwouPyM" #token
emakbot = telebot.TeleBot(token)


telegram_threading()
thread_loop()