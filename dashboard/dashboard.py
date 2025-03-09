import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set konfigurasi halaman di bagian paling atas
st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛒", layout="wide")

# Atur gaya visualisasi
sns.set_theme(style="darkgrid", context="notebook")

# Load data dari file CSV
@st.cache_data
def ambil_data():
    file_path = os.path.join(os.getcwd(), 'dashboard', 'final_data.csv')
    try:
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        else:
            st.error(f"⚠️ File CSV tidak ditemukan di path: `{file_path}`")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error saat membaca file CSV: {e}")
        return pd.DataFrame()

# Ambil data
df = ambil_data()

# Judul utama
st.title('🛒 E-Commerce Dashboard')

# Sidebar dengan opsi navigasi
st.sidebar.title('🚀 Navigasi')
sidebar_option = st.sidebar.selectbox(
    'Pilih opsi untuk ditampilkan:',
    ['Distribusi Metode Pembayaran', 'Metode Pembayaran Paling Sering Digunakan']
)

if not df.empty and 'payment_type' in df.columns:
    if sidebar_option == 'Distribusi Metode Pembayaran':
        st.subheader('📊 Distribusi Metode Pembayaran')

        # Hitung distribusi metode pembayaran dan urutkan dari terbesar ke terkecil
        payment_distribution = df['payment_type'].value_counts().sort_values(ascending=False)

        if not payment_distribution.empty:
            # Tampilkan bar chart untuk distribusi metode pembayaran (urutan terbesar di kiri)
            fig, ax = plt.subplots(figsize=(8, 5))
            payment_distribution.plot(
                kind='bar', 
                color='skyblue', 
                ax=ax
            )
            ax.set_xlabel('Metode Pembayaran')
            ax.set_ylabel('Jumlah Transaksi')
            ax.set_title('Distribusi Metode Pembayaran')

            # Rotasi label untuk keterbacaan yang lebih baik
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

            st.pyplot(fig)
        else:
            st.warning("⚠️ Tidak ada data metode pembayaran yang valid.")

    elif sidebar_option == 'Metode Pembayaran Paling Sering Digunakan':
        st.subheader('💳 Metode Pembayaran Paling Sering Digunakan')

        # Hitung distribusi metode pembayaran
        payment_distribution = df['payment_type'].value_counts()

        if not payment_distribution.empty:
            # Metode pembayaran yang paling sering digunakan
            most_common_payment = payment_distribution.idxmax()
            most_common_count = payment_distribution.max()

            # Gabungkan metode selain yang paling sering ke dalam kategori "Lainnya"
            other_count = payment_distribution.iloc[1:].sum()

            # Data untuk pie chart
            pie_data = pd.Series({
                most_common_payment: most_common_count,
                'Lainnya': other_count
            })

            st.markdown(f"Metode pembayaran yang paling sering digunakan adalah **{most_common_payment}** dengan **{most_common_count} transaksi**.")

            # Pie chart untuk metode pembayaran paling sering digunakan
            fig, ax = plt.subplots()
            pie_data.plot(
                kind='pie', 
                autopct='%1.1f%%', 
                startangle=90, 
                ax=ax, 
                colors=sns.color_palette('pastel')
            )
            ax.axis('equal')  # Supaya pie chart tidak oval
            ax.set_ylabel('')
            ax.set_title('Proporsi Metode Pembayaran')

            st.pyplot(fig)
        else:
            st.warning("⚠️ Tidak ada data metode pembayaran yang valid.")
else:
    st.error("❌ Kolom 'payment_type' tidak ditemukan atau kosong!")

# Menambahkan footer
st.markdown("""
---
Made with ❤️ by Dellanda
""")
