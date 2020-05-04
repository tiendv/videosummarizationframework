st=0
en=-1

for i in {0..10}
do
    st=$(($en+1))
    en=$(($en+23))
    if [ $en -gt 243 ]
    then
        en=243
    fi
    echo $st $en
    # CUDA_VISIBLE_DEVICES=0 python detect_event.py $st $en &
done
