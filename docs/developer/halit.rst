Halit Uğurgelen Tarafından Yapılan Kısımlar
===========================================

Burada Konular tablosunun başlangıç değerleri ile kodları anlatılmaktadır.

Bu tabloda 3 sütun bulunmaktadır (topicID, topic, description).

**Başlangıç değerleri**

*init.py* içindeki ilgili kısımda ilk tablo değerleri INSERT sorgusu içinde yer almakta olup CREATE TABLE ile oluşturulan tabloya eklenmesi yapılır:

.. code-block:: python

  def topics(self):
      with dbapi2.connect(self.cp) as connection:
          cursor = connection.cursor()
          query = "DROP TABLE IF EXISTS topics CASCADE"
          cursor.execute(query)
          query = """CREATE TABLE topics (
                  topicID SERIAL PRIMARY KEY,
                  topic VARCHAR(40) UNIQUE NOT NULL,
                  description VARCHAR(80) NOT NULL
                  )"""
          cursor.execute(query)
  
          query = """INSERT INTO topics (topic, description) VALUES
            ('Careers','Talk about careers here!'),
            ('Engineering','Talk about engineering here!'),
            ('Finance','Talk about finance here!'),
            ('International','Talk about international topics here!'),
            ('Jobs','Talk about jobs here!'),
            ('Languages','Talk about languages here!'),
            ('Miscellaneous','Talk about various stuff here!'),
            ('Technology','Talk about technology here!');
            """
          cursor.execute(query)
          connection.commit()

**İsteklerin değerlendirilmesi**

*server.py* içindeki ilgili kısımda tablo değerlerinin uygun fonksiyona yönlendirilmesi yapılır:

.. code-block:: python

  @app.route('/konular')
  def topics_page():
      tops = topics(app.config['dsn'])
      fn = Func(app.config['dsn'])
      if request.method == 'GET':
          now = datetime.datetime.now()
          tlist = tops.get_topiclist()
          return render_template('topics.html', topics = tlist, current_time = now.ctime())
      elif 'delete_selected' in request.form:
          topicids = request.form.getlist('delete_selected')
          for topicID in topicids:
              tops.delete_topic(topicID)
          return redirect(url_for('topics_page'))
      elif 'add' in request.form:
          tops.add_topic(request.form['topic'],request.form['description'])
          return redirect(url_for('topics_page'))
      elif 'update' in request.form:
          tops.update_topic(request.form['topicID'], request.form['topic'],request.form['description'])
          return redirect(url_for('topics_page'))

**Sorguların gerçeklenmesi**

*topics.py* içinde sorgu kodları ve bunların işlenmesi yer alır (liste çekme, konu ekleme/silme/güncelleme):

.. code-block:: python

	import psycopg2 as dbapi2
	
	class Topics:
	    def __init__(self, cp):
	        self.cp = cp
	        self.id = topicID
	        self.description = description
	        return
	
	    def get_topiclist(self):
	        with dbapi2.connect(self.cp) as connection:
	            cursor = connection.cursor()
	            query = "SELECT * FROM topics"
	            cursor.execute(query)
	            rows = cursor.fetchall()
	            return rows
	            
	    def delete_topic(self, topicID):
	        with dbapi2.connect(self.cp) as connection:
	            cursor = connection.cursor()
	            query = "DELETE FROM topics WHERE topicID = '%s'" % (topicID)
	            cursor.execute(query)
	            connection.commit()
	            return
	            
	    def add_topic(self, topic, description):
	        with dbapi2.connect(self.cp) as connection:
	            cursor = connection.cursor()
	            query =  "INSERT INTO topics (topic, description) VALUES ('%s','%s')" % (topic, description)
	            cursor.execute(query)
	            connection.commit()
	            return
	            
	    def update_topic(self, topicID, topic, description):
	        with dbapi2.connect(self.cp) as connection:
	            cursor = connection.cursor()
	            query =  "UPDATE topics SET topic = '%s', description = '%s' WHERE topicID='%s'" % (topic, description, topicID)
	            cursor.execute(query)
	            connection.commit()
	            return

**Arayüz**

*topics.html* içinde arayüz için kullanılan HTML kodu aşağıdaki gibidir:

.. code-block:: html

	{% extends "logged_in_layout.html" %}
	{% block title %}Konular{% endblock %}
	{% block content %}
	<div class="container text-center">
		<h1>Konular</h1>
	</div>
	<form action="{{ url_for('topics_page') }}" method="post">
		<table>
			<tr>
				<th>Seç</th>
				<th>Numara</th>
				<th>Konu</th>
				<th>Açıklama</th>
			</tr>
			
			{% for topicID, topic, description in topics %}
			<tr>
				<td><input type="checkbox" name="delete_selected" value="{{ topicID }}" /></td>
				<td>{{ topicID }}</td>
				<th>{{ topic }}</th>
				<th>{{ description }}</th>
			</tr>
			{% endfor %}
			
		</table>
		<input type="submit" value="Sil" name="delete" />
	</form>
	<h2>Konu ekle</h2>
	<span style="float:left;">
		<form action="{{ url_for('topics_page') }}" method="post">
			<table>
				<tr>
					<th>topic:</th>
					<td><input type="text" name="Konu: " required autofocus /> </td>
				</tr>
				<tr>
					<th>description:</th>
					<td><input type="text" name="Açıklama: " required autofocus /> </td>
				</tr>
			</table>
			<input type="submit" value="Ekle" name="add"/>
		</form>
	</span>
	<h2>Konu güncelle</h2>
	<span style="float:left;">
		<form action="{{ url_for('topics_page') }}" method="post">
			<table>
				<tr>
					<th>topicID:</th>
					<td><input type="text" name="Konu Numarası: " required autofocus /> </td>
				</tr>
				<th>topic:</th>
				<td><input type="text" name="Konu: " required autofocus /> </td>
				<tr>
					<th>description:</th>
					<td><input type="text" name="Açıklama: " required autofocus /> </td>
				</tr>
			</table>
			<input type="submit" value="Güncelle" name="update"/>
		</form>
	</span>
	<h2>Konu sil</h2>
	<span style="float:left;">
		<form action="{{ url_for('topics_page') }}" method="post">
			<table>
				<tr>
					<th>topicID:</th>
					<td><input type="text" name="Konu Numarası: " required autofocus /> </td>
				</tr>
			</table>
			<input type="submit" value="Sil" name="delete"/>
		</form>
	</span>
	
	{%endblock%}


