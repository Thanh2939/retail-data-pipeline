import os
import glob
import pandas as pd
from sqlalchemy import create_engine 

# ==========================================
# 1. THÔNG TIN KẾT NỐI SQL SERVER CỦA BẠN
# ==========================================
# Chữ 'r' ở đầu rất quan trọng để Python không bị lỗi với dấu gạch chéo ngược '\'
ten_server = r'DESKTOP-PJT48NR\SQL2025' 
ten_db = 'BangQuanLiKho'

# Tạo bộ động cơ kết nối (Sử dụng Windows Authentication)
chuoi_ket_noi = f"mssql+pyodbc://@{ten_server}/{ten_db}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
engine = create_engine(chuoi_ket_noi)

# ==========================================
# 2. ĐỌC VÀ XỬ LÝ DỮ LIỆU BẰNG PANDAS
# ==========================================
thu_muc_data = r'D:\DataEngineer\Dataset\csv\quan_li_kho'
ten_chua_bang = {}
danh_sach_file = glob.glob(os.path.join(thu_muc_data, '*.csv'))

print("⏳ Đang quét và đọc dữ liệu từ thư mục...")
for duong_dan in danh_sach_file:
    ten_file = os.path.basename(duong_dan)
    ten_file = os.path.splitext(ten_file)[0] # Cắt đuôi .csv
    ten_chua_bang[ten_file] = pd.read_csv(duong_dan)
a1=ten_chua_bang['annex1']
a2=ten_chua_bang['annex2']
a3=ten_chua_bang['annex3']
a4=ten_chua_bang['annex4']
a2['Thu_nhap']=a2['Quantity Sold (kilo)']*a2['Unit Selling Price (RMB/kg)']
a2_1 = a2.groupby(['Date', 'Item Code'])[['Thu_nhap', 'Quantity Sold (kilo)']].sum().reset_index()
a2_1=a2_1.merge(a3,on=['Date','Item Code'],how='left')
a2_1=a2_1.merge(a4,on='Item Code',how='left')
print(a2_1[['Date','Item Name','Thu_nhap']])
a2_1['Gia_von']=a2_1['Quantity Sold (kilo)']*a2_1['Wholesale Price (RMB/kg)']*(1+a2_1['Loss Rate (%)']/100)
a2_1['Loi Nhuan']=a2_1['Thu_nhap']-a2_1['Gia_von']
kq=a2_1.groupby('Date')['Loi Nhuan'].sum().reset_index()
print(kq)

print(f"🚀 Đang nạp dữ liệu lên Server: {ten_server}...")

for bang in ten_chua_bang:
    ten_chua_bang[bang].to_sql(bang, con=engine, if_exists='replace', index=False)
    print(f"  ✅ Đã nạp thành công bảng: {bang}")

print("\n🎉 ĐƯỜNG ỐNG ĐÃ CHẠY XONG! Hãy mở phần mềm SQL lên và Refresh lại thư mục Tables nhé.")