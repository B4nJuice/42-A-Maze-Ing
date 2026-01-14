ROOT_PROJECT_DIR="."

TEMP_DIR=$(mktemp -d)

echo "Configure temp diretory ($TEMP_DIR/).."
mkdir $TEMP_DIR/local_libs
PREFIX="$TEMP_DIR/local_libs"
export PKG_CONFIG_PATH="$PKG_CONFIG_PATH:$PREFIX/lib/pkgconfig"
export CPATH="$CPATH:$PREFIX/include"
export LIBRARY_PATH="$LIBRARY_PATH:$PREFIX/lib"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$PREFIX/lib"

echo "Create virtual environment ($ROOT_PROJECT_DIR/.venv).."
cd $ROOT_PROJECT_DIR
python3 -m venv .venv
source .venv/bin/activate
_ROOT_PROJECT_DIR = $(pwd)

echo "Download and decompress minilibx sources.."
cd $TEMP_DIR
wget https://cdn.intra.42.fr/document/document/43952/mlx_CLXV-2.2.tgz
tar xvf mlx_CLXV-2.2.tgz

echo "Download and decompress xcb-keysyms.."
cd $TEMP_DIR
wget http://deb.debian.org/debian/pool/main/x/xcb-util-keysyms/xcb-util-keysyms_0.4.1.orig.tar.xz
tar xvf xcb-util-keysyms_0.4.1.orig.tar.xz

echo "Build xcb-keysyms.."
cd xcb-util-keysyms-0.4.1/
./configure --prefix=$TEMP_DIR/local_libs
make
make install

echo "Make minilibx.."
cd $TEMP_DIR/mlx_CLXV
./configure.sh
make

echo "Pip install minilibx.."
cd $_ROOT_PROJECT_DIR
mv $TEMP_DIR/mlx_CLXV/mlx-2.2-py3-none-any.whl .
./.venv/bin/python3 -m pip install mlx-2.2-py3-none-any.whl
rm mlx-2.2-py3-none-any.whl

echo "Cleaning ($TEMP_DIR/).."
cd $_ROOT_PROJECT_DIR
rm -rf $TEMP_DIR
