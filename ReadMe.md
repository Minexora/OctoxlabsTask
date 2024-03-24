# Octoxlabs Task
Kullanıcıların login olarak entry girmesini sağlayan bir sistemdir. Projenin yapımında docker, django, elasticsearch, rest, unit test ve black teknolojileri kullanıldı.
Custom token sistemi ve elasticsearchte query string yerine **search ve Q querysi** kullanıldi. 



## Proje Kurulum

### Manuel Kurulum
> Not: Elasticsearch ve postgresql ilk önce yüklenilmelidir. Aşağıdaki işlermler server kurulumu için yapılması gerekenlerdir.

-> Environment oluşturulması için aşağıdaki terminale proje konumununa gelinerek kodu yazılmalıdır.
```bash
 python -m venv venv
```

-> Environmetin içine girilmesi gerekiyor. Bu işlem işletim sistemine göre değişkenlik göstermektedir. Aşağıdaki kodları(windows makine için) yazarak environmet içerisine girilir.
```bash
 source venv/Scripts/activate
```

-> Gerekliliklerin yüklenilmesi için aşağıdaki komut yazılmalıdır.
```bash
 pip install -r requiremets.txt
```

-> Veritabanının oluşması için aşağıdaki komutlar yazılmalıdır.
```bash
 python manage.py makemigrations # Migrationların oluşturulması için kullanılır.

 python manage.py migrate # Migrationların database uygulanması için kullanılır.
```

-> Elasticsearch içerisinde indexlerin oluşturulması için aşağıdaki komut yazılmalıdır.
```bash
 python manage.py search_index --rebuild
```

-> Yukarıdaki kurulum işlemleri yapıldıktan sonra aşağıdaki kod yazılarak projeyi ayağa kaldırılır.
```bash
 python manage.py runserver 0.0.0.0:8000
```

-> Curl üzerinde json veriyi formatlı görmek istiyorsak aşağıdaki komutu yazılmalıdır.
```bash
 curl -u <KullanıcıAdı>:"<Parola>" -X GET "http://localhost:9200/entries/_search" |  python -m json.tool
```

### Docker Kurulumu
**"docker-compose.yml"** dosyası içerisinde herşey ayarlanmıştır. Aşağıdaki konut yazılarak tüm gereklilikler yüklenip daha sonrasında proje run edilir.
```bash
docker-compose up --build -d 
```

## Proje Detayları

### Login Yapısı ve Authentication Yapısı
Login olabilmek için **"{baseUrl}/api/login"** urline istek atılır.Dönen response ta **access_token,refresh_token** token bilgileri gelmektedir.
Diğer urllere istek atılırken headerı aşağıdaki gibi ayarlayarak gönderilmesi gerekmektedir. 
```
HTTP_AUTHORIZATION="octoxlabs access_token"
```
Authentication yapısında **octoxlabs** adında custom token type kullanılıyor. Bu yapılan işlemleri **"authentication.py"** dosyası içerisinden 
görebilirsiniz. Access tokenin expire olması durumunda **"{baseUrl}/api/refresh-token"** urline request bodysini aşağıdaki gibi doldurulup
gönderilmesi durumunda yeni access token elde edilir. Token süreleri config dosyasında yer almaktadır.
```json
{
 "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3MTM4Nzg0MzQsImlhdCI6MTcxMTI4NjQzNH0.9LFNJuqjvIZki6HcVC38TGp6wft_o3sQM0zcPzYaUyU"
}
```

### Sorgulama 
Elasticsearch içerisinde arama yapmak için **"{baseUrl}/api/search"** urline istek atılır.Sorgularda büyük-küçük harf duyarlılığı vardır.
Request bodysi aşağıdaki gibidir. Sorgulama da **query** içerisene ',' kullanılarak birden fazla sorugu yazılabilir şekilde ayarlandı.
```json
{
 "query": "subject = deneme*"
}
```


### Django Admin Paneli
Tüm verileri yönetebilmek için djangonun admin paneli kullanılabilir.Admin paneline **"{baseUrl}/admin"** adresinden ulaşılabilir.
Kullanıcı bilgileri:
```
Username: octoAdmin
Password: 159951
```

### Testlerin Çalışması
Apilerin testlerini yapmak için aşağıdaki komut terminale yazılmalıdır.
```bash
python manage.py test .
```

### Management Command
Management Command olarak tüm entry listesini güncel tarihe göre sıralayarak consola yazacak şekilde ayarlandı.
Amacı elasticsearchte arama yapıldığında verilerin doğru gelip gelmediğini kontrol etmektir.

 ```bash
 python manage.py listallentry
```
 

### Quality Tool
Quality tool olarak black kullanılmakatadır. Kodları yeniden formatlamak için aşağıdaki komut terminale yazılmalıdır.
```bash
 black .
```