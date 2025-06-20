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

# tomli kütüphanesini kontrol et ve yükle
if ! python -c "import tomli" 2>/dev/null; then
    echo "tomli kütüphanesi bulunamadı, yükleniyor..."
    python -m pip install tomli --user
    if [ $? -ne 0 ]; then
        echo "tomli kütüphanesi yüklenemedi, alternatif yöntem deneniyor..."
        python -m pip install toml --user
        if [ $? -ne 0 ]; then
            echo "toml kütüphanesi de yüklenemedi!"
            exit 1
        else
            # Versiyon numarasını pyproject.toml dosyasından al (toml ile)
            version=$(python -c "import toml; print(toml.load('pyproject.toml')['project']['version'])")
            if [ -z "$version" ]; then
                echo "Versiyon numarası alınamadı!"
                exit 1
            fi
        fi
    else
        # Versiyon numarasını pyproject.toml dosyasından al (tomli ile)
        version=$(python -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])")
        if [ -z "$version" ]; then
            echo "Versiyon numarası alınamadı!"
            exit 1
        fi
    fi
else
    # Versiyon numarasını pyproject.toml dosyasından al (tomli ile)
    version=$(python -c "import tomli; print(tomli.load(open('pyproject.toml', 'rb'))['project']['version'])")
    if [ -z "$version" ]; then
        echo "Versiyon numarası alınamadı!"
        exit 1
    fi
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
