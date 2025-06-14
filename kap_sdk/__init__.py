def _get_browser_config():
    """Tarayıcı yapılandırmasını döndüren ortak metod.
    Tüm launch işlemleri için kullanılabilir.
    """
    return {
        'handleSIGINT': "false",
        'handleSIGTERM': "false",
        'handleSIGHUP': "false",
        'headless': True,
        'args': [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process'
        ]
    }
