import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fpdf import FPDF
import os


# URL của trang danh mục (ví dụ: Khoa học công nghệ)
base_url = "https://dantri.com.vn/khoa-hoc-cong-nghe.htm"

# Thư mục để lưu file PDF
output_folder = r"D:\thaythedoanpj1\khoahoccongnghe"
os.makedirs(output_folder, exist_ok=True)

# Hàm để lấy liên kết bài báo từ một trang
def get_article_links(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for h3_tag in soup.find_all('h3', class_='article-title'):
        a_tag = h3_tag.find('a')
        if a_tag and a_tag['href'].startswith('/'):
            links.append("https://dantri.com.vn" + a_tag['href'])
    return links

# Hàm lưu bài báo dưới dạng PDF với font Unicode
def save_article_as_pdf(index, title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Đảm bảo font được thêm đúng cách cho cả style thường và đậm
    pdf.add_font('DejaVu', '', 'font\DejaVuSans.ttf', uni=True)  # Thêm font thường
    pdf.add_font('DejaVu', 'B', 'font\DejaVuSans-Bold.ttf', uni=True)  # Thêm font đậm

    # Tiêu đề với font đậm
    pdf.set_font('DejaVu', 'B', size=16)
    pdf.cell(0, 10, f"Title: {title}", ln=True, align='L')
    pdf.ln(10)

    # Nội dung với font thường
    pdf.set_font('DejaVu', '', size=12)
    pdf.multi_cell(0, 10, content)

    # Tên file PDF (số thứ tự)
    filename = os.path.join(output_folder, f"{index}.pdf")
    pdf.output(filename)
    print(f"Đã lưu bài báo thành PDF: {filename}")

# Duyệt qua các trang và lấy bài báo từ các trang đó
index = 1
for page_number in range(1, 6):  # Lặp qua 5 trang (trang 1 đến trang 5)
    if page_number == 1:
        page_url = base_url  # Trang 1 có URL riêng
    else:
        page_url = f"https://dantri.com.vn/xa-hoi/trang-{page_number}.htm"  # Các trang tiếp theo
    
    print(f"Đang tải trang {page_number}...")
    
    # Lấy liên kết bài báo từ trang hiện tại
    links = get_article_links(page_url)
    
    # Duyệt qua các bài báo và lưu chúng thành PDF
    for link in links:
        article_response = requests.get(link)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        
        # Lấy tiêu đề
        title_tag = article_soup.find('h1', class_='title-page')
        title = title_tag.text.strip() if title_tag else "Không có tiêu đề"
        
        # Lấy nội dung bài báo
        content_tag = article_soup.find('div', class_='singular-content')
        content = content_tag.text.strip() if content_tag else "Không có nội dung"
        
        # Lưu bài báo thành PDF
        save_article_as_pdf(index, title, content)
        index += 1  # Tăng số thứ tự cho bài báo tiếp theo

print(f"Tất cả bài báo đã được lưu tại {output_folder}")
