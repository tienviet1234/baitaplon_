#  Trình Thu Thập Dữ Liệu Bất Động Sản Tự Động từ Alonhadat.com.vn

##  Giới thiệu

Dự án này là một **trình thu thập dữ liệu (web crawler)** sử dụng **Python và Selenium WebDriver** để tự động truy cập vào website [https://alonhadat.com.vn](https://alonhadat.com.vn), áp dụng bộ lọc tìm kiếm bất động sản theo khu vực **Đà Nẵng** và nhu cầu **Cho thuê**, trích xuất thông tin của các bài đăng, và lưu lại dữ liệu dưới dạng **file Excel (.xlsx)**.

Ngoài ra, chương trình có khả năng **lên lịch tự động chạy mỗi ngày lúc 06:00 sáng**, rất phù hợp để tự động cập nhật dữ liệu hàng ngày phục vụ cho các ứng dụng phân tích hoặc theo dõi thị trường.

---

##  Tính năng chính

1) Tự động mở trình duyệt và truy cập Alonhadat.com.vn
def khoi_tao_trinh_duyet():
    trinh_duyet = webdriver.Chrome()
    trinh_duyet.get("https://alonhadat.com.vn/")
    trinh_duyet.maximize_window()
    return trinh_duyet
2) Áp dụng bộ lọc: Thành phố Đà Nẵng, nhu cầu Cho thuê
def ap_dung_bo_loc(trinh_duyet, doi):
    thanh_pho = Select(doi.until(EC.presence_of_element_located((By.CLASS_NAME, "province"))))
    thanh_pho.select_by_visible_text("Đà Nẵng")

    nhu_cau = Select(doi.until(EC.presence_of_element_located((By.CLASS_NAME, "demand"))))
    nhu_cau.select_by_visible_text("Cho thuê")

    nut_tim_kiem = doi.until(EC.element_to_be_clickable((By.CLASS_NAME, "btnsearch")))
    nut_tim_kiem.click()
    time.sleep(3)

3) Trích xuất thông tin gồm: Tiêu đề, Mô tả, Diện tích, Giá, Địa chỉ, Hình ảnh, Link chi tiết
def trich_xuat_du_lieu_trang(trinh_duyet):
    tieu_de = trinh_duyet.find_elements(By.CSS_SELECTOR, ".ct_title a")
    mo_ta = trinh_duyet.find_elements(By.CSS_SELECTOR, ".ct_brief")
    ...
    for i in range(len(tieu_de)):
        du_lieu = {
            "Tiêu đề": tieu_de[i].text,
            "Mô tả": mo_ta[i].text if i < len(mo_ta) else "",
            ...
        }

4) Duyệt và thu thập dữ liệu từ nhiều trang (tối đa cấu hình)
def thu_thap_du_lieu(trinh_duyet, doi, so_trang_toi_da=5):
    for trang_hien_tai in range(1, so_trang_toi_da + 1):
        ...
        nut_tiep = doi.until(EC.presence_of_element_located((By.LINK_TEXT, ">>")))
        if "disabled" in nut_tiep.get_attribute("class"):
            break
        nut_tiep.click()
        time.sleep(3)

5) Lưu dữ liệu vào file Excel có cấu trúc rõ ràng
def luu_vao_excel(du_lieu, duong_dan_file):
    df = pd.DataFrame(du_lieu)
    df.to_excel(duong_dan_file, index=False, engine='openpyxl')

-  Lên lịch chạy tự động đúng 06:00 mỗi ngày
if __name__ == "__main__":
    while True:
        bay_gio = datetime.now()
        if bay_gio.hour == 6 and bay_gio.minute == 00:
            chay_trinh_thu_thap()
            time.sleep(70)
        else:
            time.sleep(30)

---

##  Công nghệ sử dụng

- Python 3.x
- [Selenium](https://pypi.org/project/selenium/)
- [pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/)
- Trình duyệt: Google Chrome
- ChromeDriver (phù hợp với phiên bản Chrome)

---

## ⚙️ Hướng dẫn cài đặt

### 1. Cài đặt Python và các thư viện

- Tải Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Cài đặt các thư viện cần thiết:
```bash
pip install selenium pandas openpyxl