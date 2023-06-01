from flask import redirect, url_for, Flask, render_template, request
import mysql.connector
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

app = Flask(__name__)

# Mengatur koneksi ke database MySQL
try:
    db = mysql.connector.connect(
        host="localhost",
        user="imam",
        password="Aceh2033",
        database="uas_km"
    )
    print("Connected to database successfully!")
except mysql.connector.Error as error:
    print("Failed to connect to database:", error)

# Membaca file keyword_map.txt


def read_keyword_map(keyword_map_path):
    keyword_map = {}
    with open(keyword_map_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(":")
                category = parts[0].strip()
                keywords = [keyword.strip() for keyword in parts[1].split(",")]
                keyword_map[category] = keywords
    return keyword_map


# Membaca keyword_map.txt saat aplikasi dimulai
keyword_map_path = "static/data/keyword_map.txt"
keyword_map = read_keyword_map(keyword_map_path)

# Membuat tabel extracted_knowledge jika belum ada


def create_table():
    cursor = db.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS extracted_knowledge (category VARCHAR(255), sentence TEXT, accuracy FLOAT)")


# Menjalankan fungsi create_table() saat aplikasi dimulai
create_table()

# Menangani halaman utama


@app.route('/')
def index():
    return render_template('index.html')


# Menangani halaman hasil ekstraksi pengetahuan
@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        text = request.form['text']

        # Memanggil fungsi untuk ekstraksi pengetahuan
        extraction_results = extract_knowledge(text)

        # Memasukkan pengetahuan eksplisit ke database dan menghitung akurasi
        insert_extracted_knowledge(extraction_results)

        # Redirect ke halaman hasil (GET request)
        return redirect(url_for('result'))
    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM extracted_knowledge")
        extraction_results = [
            {'category': row[0], 'sentence': row[1], 'accuracy': row[2]} for row in cursor.fetchall()]

        # Mendapatkan kategori yang tersedia dalam tabel
        cursor.execute("SELECT DISTINCT category FROM extracted_knowledge")
        categories = [row[0] for row in cursor.fetchall()]

        # Mendapatkan kategori terpilih dari permintaan GET
        selected_category = request.args.get('category')

        # Mengambil hasil ekstraksi pengetahuan berdasarkan kategori terpilih
        if selected_category:
            cursor.execute(
                "SELECT * FROM extracted_knowledge WHERE category = %s", (selected_category,))
            extraction_results = [
                {'category': row[0], 'sentence': row[1], 'accuracy': row[2]} for row in cursor.fetchall()]

        # Menghitung jumlah pengetahuan yang diekstraksi dari setiap kategori
        knowledge_count = {}
        for result in extraction_results:
            category = result['category']
            if category in knowledge_count:
                knowledge_count[category] += 1
            else:
                knowledge_count[category] = 1

        # Membuat data untuk grafik
        labels = list(knowledge_count.keys())
        data = list(knowledge_count.values())

        return render_template('result.html', extraction_results=extraction_results, categories=categories, selected_category=selected_category, labels=labels, data=data)


# Menangani halaman visualisasi
@app.route('/visual')
def visual():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM extracted_knowledge")
    extraction_results = [
        {'category': row[0], 'sentence': row[1], 'accuracy': row[2]} for row in cursor.fetchall()]

    # Mendapatkan kategori yang tersedia dalam tabel
    cursor.execute("SELECT DISTINCT category FROM extracted_knowledge")
    categories = [row[0] for row in cursor.fetchall()]

    # Mendapatkan kategori terpilih dari permintaan GET
    selected_category = request.args.get('category')

    # Mengambil hasil ekstraksi pengetahuan berdasarkan kategori terpilih
    if selected_category:
        cursor.execute(
            "SELECT * FROM extracted_knowledge WHERE category = %s", (selected_category,))
        extraction_results = [
            {'category': row[0], 'sentence': row[1], 'accuracy': row[2]} for row in cursor.fetchall()]

    # Menghitung jumlah pengetahuan yang diekstraksi dari setiap kategori
    knowledge_count = {}
    for result in extraction_results:
        category = result['category']
        if category in knowledge_count:
            knowledge_count[category] += 1
        else:
            knowledge_count[category] = 1

    # Membuat data untuk grafik
    labels = list(knowledge_count.keys())
    data = list(knowledge_count.values())

    return render_template('visual.html', extraction_results=extraction_results, categories=categories, selected_category=selected_category, labels=labels, data=data)


# Ekstraksi pengetahuan menggunakan pemrosesan bahasa alami (NLP)
def extract_knowledge(text):
    sentences = sent_tokenize(text)

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stop_words = set(stopwords.words("indonesian"))

    extracted_knowledge = []

    for sentence in sentences:
        words = word_tokenize(sentence)
        filtered_words = [stemmer.stem(word.lower()) for word in words if word.isalnum(
        ) and word.lower() not in stop_words]
        category = classify_category(filtered_words)
        accuracy = calculate_accuracy(filtered_words, category)
        extracted_knowledge.append({
            'sentence': sentence,
            'category': category,
            'accuracy': accuracy
        })

    return extracted_knowledge


# Klasifikasi kategori ilmu
def classify_category(extracted_knowledge):
    category = "unknown"  # Kategori awal

    # Memeriksa setiap kategori dan mencocokkan kata kunci
    for category_name, keywords in keyword_map.items():
        if any(keyword in extracted_knowledge for keyword in keywords):
            category = category_name
            break

    return category


# Menghitung akurasi berdasarkan kategori yang diklasifikasikan
def calculate_accuracy(extracted_knowledge, classified_category):
    reference_keywords = keyword_map.get(classified_category, [])
    extracted_keywords = [
        word for word in extracted_knowledge if word in reference_keywords]
    accuracy = len(extracted_keywords) / \
        len(reference_keywords) if len(reference_keywords) > 0 else 0
    return accuracy


# Memasukkan pengetahuan eksplisit ke database
def insert_extracted_knowledge(extraction_results):
    cursor = db.cursor()

    # Menjalankan perintah SQL untuk memasukkan data ke tabel
    sql = "INSERT INTO extracted_knowledge (category, sentence, accuracy) VALUES (%s, %s, %s)"
    values = [(result['category'], result['sentence'], result['accuracy'])
              for result in extraction_results]
    cursor.executemany(sql, values)

    # Melakukan commit untuk menyimpan perubahan
    db.commit()


# Reset database route
@app.route('/reset', methods=['POST'])
def reset():
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS extracted_knowledge")
    create_table()
    return redirect(url_for('result', notification="Database reset successfully!"))


# Menjalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True)
