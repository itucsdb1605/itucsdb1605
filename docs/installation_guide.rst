Kurulum Kılavuzu
================

Projeyi doğru şekilde çalıştırabilmek için aşağıda belirtilen paketler ve programlar yüklenmelidir.

**Python 3.4.3**

Python bu linkten yüklenebilir: https://www.python.org/downloads/release/python-343/Don

**Flask Framework**

Flask bu linkten yüklenebilir: http://pypi.python.org/packages/source/F/Flask/Flask-0.10.1.tar.gz

YADA pip aracılığıyla yüklenebilir.

.. code-block:: python
	
	pip install Flask

**Psycopg2**

Psycopg2 bu linkten yüklenebilir: http://www.stickpeople.com/projects/python/win-psycopg/

YADA pip aracılığıyla yüklenebilir.

.. code-block:: python
	
	pip install psycopg2

**PostgreSQL**

PostgreSQL bu linkten yüklenebilir: http://www.postgresql.org/download/

.. code-block:: python

	if __name__ == '__main__':
	    app.secret_key = '\xd1M<n)\xf1\xf9\x08\xe2z\x8ai\x99\xf8\xb8\xf0\xe9\x06\x95"0\x9d\xd2\xf9'
	    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
	    if VCAP_APP_PORT is not None:
	        port, debug = int(VCAP_APP_PORT), False
	    else:
	        port, debug = 5000, True

	    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
	    if VCAP_SERVICES is not None:
	        app.config['dsn'] = get_sqldb_dsn(VCAP_SERVICES)
	    else:
	        app.config['dsn'] = """dbname='your_choice' host='localhost' port=your_choice user='your_choice' password='your_choice'"""

	    if not os.path.exists('static/personphotos/'):
	        os.makedirs('static/personphotos/')

	    app.run(host='0.0.0.0', port=port, debug=debug)

**server.py Çalıştırma**

Komut satırında projenin yoluna gidilerek aşağıdaki komut çalıştırılır.

.. code-block:: python
	
	python server.py
