if [[ $(pidof pigpiod) ]]; then
  echo "pigpiod already on"
else
  sudo pigpiod
fi

python3 -m flask run --host=0.0.0.0
