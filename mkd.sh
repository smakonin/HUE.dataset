n=1;
max=200;
while [ "$n" -le "$max" ]; do
  mkdir "house_$n"
  n=`expr "$n" + 1`;
done

