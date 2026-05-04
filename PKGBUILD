pkgname=lufus-git
pkgver=1.1.5
pkgrel=2
pkgdesc="Minimalist GUI tool to create bootable USB drives"
arch=('any')
url="https://github.com/Advnirr/lufus"
license=('GPL3')
depends=('python-gobject' 'gtk4' 'libadwaita' 'wimlib' 'rsync' 'parted' 'polkit' 'libarchive')
makedepends=('git')
source=("main.py" "windows_logic.py" "universal_logic.py" "lufus.desktop" "lufus.svg")
sha256sums=('SKIP' 'SKIP' 'SKIP' 'SKIP' 'SKIP')

package() {
    install -d "${pkgdir}/usr/share/lufus"
    
    install -Dm755 "${srcdir}/main.py" "${pkgdir}/usr/share/lufus/main.py"
    install -Dm644 "${srcdir}/windows_logic.py" "${pkgdir}/usr/share/lufus/windows_logic.py"
    install -Dm644 "${srcdir}/universal_logic.py" "${pkgdir}/usr/share/lufus/universal_logic.py"
    
    install -Dm644 "${srcdir}/lufus.desktop" "${pkgdir}/usr/share/applications/lufus.desktop"
    install -Dm644 "${srcdir}/lufus.svg" "${pkgdir}/usr/share/icons/hicolor/scalable/apps/lufus.svg"
}
