#!/bin/bash

# Bu betik, Git repository'sinde versiyon kontrolü yapmak ve release oluşturmak için kullanılır.

# 1. Git işlemleri
echo "Git işlemleri başlatılıyor..."
git add .
git commit -m "Publish to PyPI"
if [ $? -ne 0 ]; then
    echo "Git commit başarısız oldu!"
    exit 1
fi
git push origin main
if [ $? -ne 0 ]; then
    echo "Git push başarısız oldu!"
    exit 1
fi

# Versiyon numarasını pyproject.toml dosyasından al
version=$(uv python run python -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])")
if [ -z "$version" ]; then
    echo "Versiyon numarası alınamadı!"
    exit 1
fi

# Versiyon tag'i oluştur ve gönder
echo "Versiyon tag'i oluşturuluyor: v$version"
git tag -a v$version -m "Release version $version"
if [ $? -ne 0 ]; then
    echo "Git tag oluşturma başarısız oldu!"
    exit 1
fi
git push origin v$version
if [ $? -ne 0 ]; then
    echo "Git tag push başarısız oldu!"
    exit 1
fi
git push --tags
if [ $? -ne 0 ]; then
    echo "Git tags push başarısız oldu!"
    exit 1
fi

echo "Release oluşturma işlemi başarıyla tamamlandı!"
