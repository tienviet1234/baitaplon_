from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime
import os

# === Hàm khởi tạo trình duyệt ===
def khoi_tao_trinh_duyet():
    trinh_duyet = webdriver.Chrome()
    trinh_duyet.get("https://alonhadat.com.vn/")
    trinh_duyet.maximize_window()
    return trinh_duyet

# === Hàm chọn bộ lọc tìm kiếm ===
def ap_dung_bo_loc(trinh_duyet, doi):
    thanh_pho = Select(doi.until(EC.presence_of_element_located((By.CLASS_NAME, "province"))))
    thanh_pho.select_by_visible_text("Đà Nẵng")

    nhu_cau = Select(doi.until(EC.presence_of_element_located((By.CLASS_NAME, "demand"))))
    nhu_cau.select_by_visible_text("Cho thuê")

    nut_tim_kiem = doi.until(EC.element_to_be_clickable((By.CLASS_NAME, "btnsearch")))
    nut_tim_kiem.click()
    time.sleep(3)

# === Hàm trích xuất dữ liệu từ một trang ===
def trich_xuat_du_lieu_trang(trinh_duyet):
    tieu_de = trinh_duyet.find_elements(By.CSS_SELECTOR, ".ct_title a")
    mo_ta = trinh_duyet.find_elements(By.CSS_SELECTOR, ".ct_brief")
    dien_tich = trinh_duyet.find_elements(By.CSS_SELECTOR, ".ct_dt")
    gia = trinh_duyet.find_elements(By.CSS_SELECTOR, ".ct_price")
    dia_chi = trinh_duyet.find_elements(By.CSS_SELECTOR, ".ct_dis")
    hinh_anh = trinh_duyet.find_elements(By.CSS_SELECTOR, ".thumbnail > a > img")

    du_lieu_trang = []

    for i in range(len(tieu_de)):
        try:
            du_lieu = {
                "Tiêu đề": tieu_de[i].text,
                "Mô tả": mo_ta[i].text if i < len(mo_ta) else "",
                "Diện tích": dien_tich[i].text if i < len(dien_tich) else "",
                "Giá": gia[i].text if i < len(gia) else "",
                "Địa chỉ": dia_chi[i].text if i < len(dia_chi) else "",
                "Hình ảnh": hinh_anh[i].get_attribute("src") if i < len(hinh_anh) else "",
                "Link chi tiết": tieu_de[i].get_attribute("href")
            }
            du_lieu_trang.append(du_lieu)
        except Exception as e:
            print(f"Lỗi ở tin số {i}: {e}")
    return du_lieu_trang

# === Hàm xử lý chuyển trang và gom dữ liệu ===
def thu_thap_du_lieu(trinh_duyet, doi, so_trang_toi_da=5):
    tat_ca_du_lieu = []

    for trang_hien_tai in range(1, so_trang_toi_da + 1):
        print(f"Đang xử lý trang {trang_hien_tai}")
        tat_ca_du_lieu.extend(trich_xuat_du_lieu_trang(trinh_duyet))

        try:
            nut_tiep = doi.until(EC.presence_of_element_located((By.LINK_TEXT, ">>")))
            if "disabled" in nut_tiep.get_attribute("class") or not nut_tiep.is_enabled():
                break
            nut_tiep.click()
            time.sleep(3)
        except Exception as e:
            print("Không thể chuyển trang hoặc đã hết trang:", e)
            break

    return tat_ca_du_lieu

# === Hàm lưu dữ liệu vào Excel ===
def luu_vao_excel(du_lieu, duong_dan_file):
    os.makedirs(os.path.dirname(duong_dan_file), exist_ok=True)
    df = pd.DataFrame(du_lieu)
    df.to_excel(duong_dan_file, index=False, engine='openpyxl')
    print(f"Đã lưu {len(du_lieu)} dòng dữ liệu vào {duong_dan_file}")

# === Hàm chính để chạy crawler ===
def chay_trinh_thu_thap():
    print("Bắt đầu thu thập dữ liệu lúc", datetime.now().strftime("%H:%M:%S"))

    trinh_duyet = khoi_tao_trinh_duyet()
    doi = WebDriverWait(trinh_duyet, 10)

    try:
        ap_dung_bo_loc(trinh_duyet, doi)
        du_lieu = thu_thap_du_lieu(trinh_duyet, doi, so_trang_toi_da=5)
        duong_dan_file = "C:\\Users\\ASUS-PRO\\Documents\\BAITAPLON\\file_luu.xlsx"
        luu_vao_excel(du_lieu, duong_dan_file)
    finally:
        trinh_duyet.quit()

# === Lên lịch chạy lúc 06:00 sáng ===
if __name__ == "__main__":
    print("Hệ thống đang chờ đến 06:00 để chạy trình thu thập dữ liệu...")

    while True:
        bay_gio = datetime.now()
        if bay_gio.hour == 6 and bay_gio.minute == 00:
            chay_trinh_thu_thap()
            time.sleep(70)  # tránh chạy lại trong cùng phút
        else:
            time.sleep(30)
