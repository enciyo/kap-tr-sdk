# kap_sdk

KAP (Kamuyu Aydınlatma Platformu) üzerinden veri çekmek için bir Python SDK'sı.

## Kurulum

kap_sdk'yı PyPI üzerinden kolayca yükleyebilirsiniz:

```bash
pip install kap_sdk
```

## Bağımlılıklar

kap_sdk aşağıdaki kütüphanelere bağımlıdır:

- **requests**: HTTP istekleri yapmak için.
- **beautifulsoup4**: HTML içeriğini ayrıştırmak için.
- **pyppeteer**: Web sayfalarını tarayıcı üzerinden işlemek için.

Bu bağımlılıklar, kap_sdk'yı yüklediğinizde otomatik olarak yüklenir.

## Kullanım

kap_sdk, KAP üzerinden şirket bilgileri, finansal raporlar, endeksler, duyurular ve sektörler gibi verilere erişim sağlar. Aşağıda, SDK'nın temel işlevlerini gösteren örnekler bulunmaktadır.

### Temel Kullanım Örneği

```python
import asyncio
from kap_sdk.kap_client import KapClient

async def main():
    # KapClient'ı başlat
    client = KapClient(
        cache_expiry=3600,           # Genel önbellek süresi (1 saat)
        company_cache_expiry=86400,  # Şirket verileri için önbellek süresi (1 gün)
        indices_cache_expiry=86400,  # Endeks verileri için önbellek süresi (1 gün)
        sectors_cache_expiry=86400   # Sektör verileri için önbellek süresi (1 gün)
    )
    
    # Şirket bilgilerini al
    company = await client.get_company("BIMAS")
    print(f"Şirket: {company.name} ({company.code}) - Şehir: {company.city}")
    
    # Şirket detay bilgilerini al
    info = await client.get_company_info(company)
    print(f"Şirket Detayları: {info}")
    
    # Finansal raporu al
    report = await client.get_financial_report(company, "2022")
    print(f"Finansal Rapor (2022): {report}")
    
    # Endeksleri al
    indices = await client.get_indices()
    print(f"Endeksler: {indices}")
    
    # Şirkete özel duyuruları al
    announcements = await client.get_announcements(company)
    print(f"Duyurular: {announcements}")
    
    # Tüm duyuruları al
    all_announcements = await client.get_announcements()
    print(f"Tüm Duyurular: {all_announcements}")
    
    # Sektörleri al
    sectors = await client.get_sectors()
    print(f"Sektörler: {sectors}")
    
    # Önbelleği temizle
    client.clear_cache()
    print("Önbellek temizlendi.")

if __name__ == "__main__":
    asyncio.run(main())
```

### İleri Düzey Kullanım

#### Özel Tarih Aralığı ile Duyuruları Alma

```python
import asyncio
from datetime import datetime, timedelta
from kap_sdk.kap_client import KapClient

async def get_announcements_with_date_range():
    client = KapClient()
    company = await client.get_company("BIMAS")
    
    # Son 7 günün duyurularını al
    from_date = datetime.today().date() - timedelta(days=7)
    to_date = datetime.today().date()
    
    announcements = await client.get_announcements(
        company=company,
        fromdate=from_date,
        todate=to_date
    )
    
    print(f"Son 7 günün duyuruları ({company.code}): {announcements}")

if __name__ == "__main__":
    asyncio.run(get_announcements_with_date_range())
```

#### Önbellekleme Sürelerini Özelleştirme

kap_sdk, farklı veri türleri için önbellekleme sürelerini özelleştirmenize olanak tanır. Örneğin, şirket verileri gibi nadiren değişen veriler için daha uzun bir önbellekleme süresi kullanabilirsiniz:

```python
import asyncio
from kap_sdk.kap_client import KapClient

async def custom_cache_expiry():
    # Şirket verileri için 1 hafta, diğer veriler için 1 saat önbellekleme
    client = KapClient(
        cache_expiry=3600,           # Genel önbellek süresi (1 saat)
        company_cache_expiry=604800, # Şirket verileri için önbellek süresi (1 hafta)
        indices_cache_expiry=86400,  # Endeks verileri için önbellek süresi (1 gün)
        sectors_cache_expiry=86400   # Sektör verileri için önbellek süresi (1 gün)
    )
    
    companies = await client.get_companies()
    print(f"Şirketler (uzun önbellekleme): {len(companies)} şirket bulundu.")
    
    # Önbelleği manuel olarak temizleme
    client.clear_cache()
    print("Önbellek temizlendi.")

if __name__ == "__main__":
    asyncio.run(custom_cache_expiry())
```

## Hata Yönetimi

kap_sdk, veri çekme işlemleri sırasında oluşabilecek hataları yakalar ve loglar. Hataları yakalamak için try-except blokları kullanabilirsiniz:

```python
import asyncio
import logging
from kap_sdk.kap_client import KapClient

# Loglamayı yapılandır
logging.basicConfig(level=logging.INFO)

async def handle_errors():
    client = KapClient()
    try:
        company = await client.get_company("BIMAS")
        report = await client.get_financial_report(company, "2022")
        print(f"Finansal Rapor: {report}")
    except Exception as e:
        logging.error(f"Bir hata oluştu: {e}")
        print("Hata oluştu, detaylar için loglara bakın.")

if __name__ == "__main__":
    asyncio.run(handle_errors())
```

## Katkıda Bulunma

kap_sdk açık kaynaklı bir projedir. Hataları bildirmek, özellik önerileri sunmak veya kod katkısında bulunmak için lütfen GitHub deposunu ziyaret edin:

[GitHub - kap_sdk](https://github.com/kullanıcı_adı/kap_sdk)

## Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına bakın.
