## Flask Ekstraksi Pengetahuan NLP

Ini adalah aplikasi web Flask yang melakukan ekstraksi pengetahuan menggunakan teknik pemrosesan bahasa alami (NLP). Aplikasi ini mengekstraksi pengetahuan eksplisit dari teks yang diberikan dan mengklasifikasikannya ke dalam kategori yang telah ditentukan berdasarkan file pemetaan kata kunci. Pengetahuan yang diekstraksi disimpan dalam database MySQL dan dapat divisualisasikan melalui antarmuka web.

### Persiapan dan Instalasi

1. Install dependensi yang diperlukan dengan menjalankan perintah berikut:
   ```
   pip install flask mysql-connector-python nltk Sastrawi
   ```

2. Buat database MySQL dan perbarui konfigurasi database dalam kode berikut:
   ```python
   db = mysql.connector.connect(
       host="localhost",
       user="imam",
       password="12345",
       database="uas_km"
   )
   ```

3. Buat file dengan nama `keyword_map.txt` di direktori `static/data`. File ini harus berisi pemetaan kategori ke kata kunci dalam format berikut:
   ```
   astronomi: planet, matahari, bulan, permukaan bumi, galaksi, bintang, orbit, tata surya, teleskop, planetarium, astrofisika, supernova, kosmologi, asteroid, komet, meteor
   geografi: daratan, lautan, atmosfer, gunung, sungai, pulau, gletser, peta, iklim, benua, gunung berapi, lembah, hutan, perairan, badai, cuaca, pemanasan global, keanekaragaman hayati, ekosistem, geologi
   ...
   ```

4. Jalankan aplikasi Flask:
   ```
   python app.py
   ```

5. Buka browser dan kunjungi `http://localhost:5000` untuk mengakses aplikasi.

### Fungsionalitas

Aplikasi Flask menyediakan fungsionalitas berikut:

1. **Halaman Utama** (`/`): Menampilkan halaman utama aplikasi.

2. **Hasil Ekstraksi Pengetahuan** (`/result`):
   - **GET**: Menampilkan pengetahuan yang diekstraksi dari database. Menampilkan kategori, kalimat, dan akurasi dari setiap pengetahuan yang diekstraksi.
   - **POST**: Menerima teks input, melakukan ekstraksi pengetahuan, memasukkan pengetahuan yang diekstraksi ke dalam database, dan mengarahkan ke halaman hasil (permintaan GET).

3. **Visualisasi Pengetahuan** (`/visual`): Menampilkan visualisasi dari pengetahuan yang diekstraksi. Menampilkan diagram batang dengan jumlah pengetahuan yang diekstraksi untuk setiap kategori. Anda dapat memfilter visualisasi berdasarkan kategori tertentu.

4. **Reset Database** (`/reset`): Mengatur ulang database dengan menghapus tabel yang ada dan membuat tabel baru.

### Struktur File

Aplikasi ini memiliki struktur file berikut:

```
- app.py               : Aplikasi Flask utama
- static/
  - data/
    - keyword_map.txt  : File yang berisi pemetaan kategori ke kata kunci
- templates/
  - index.html         : Template HTML untuk halaman utama
  - result.html        : Template HTML untuk halaman hasil ekstraksi pengetahuan
  - visual.html        : Template HTML untuk halaman visualisasi pengetahuan
```

### Pustaka yang Digunakan

- Flask: Framework web untuk membangun aplikasi.
- mysql-connector-python: Penghubung untuk database MySQL.
- nltk: Toolkit pemrosesan bahasa alami untuk tokenis

asi dan penghapusan kata berhenti.
- Sastrawi: Pustaka stemming untuk bahasa Indonesia.

### Kredit

Aplikasi ini dikembangkan oleh [Imam](https://github.com/bukanmakmum) sebagai bagian dari proyek kursus Manajemen Pengetahuan.

### Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE).
