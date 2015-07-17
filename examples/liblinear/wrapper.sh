c=$1
linear=/home/lijm/jianfei/experiments/third_party/liblinear-2.01/train
train_file=/home/lijm/jianfei/experiments/third_party/liblinear-2.01/heart_scale
output=`$linear -v 5 -c $c $train_file`
accuracy=`echo $output | tail -n 1 | sed -e 's/%/ /' | awk '{print $NF}'`
echo "accuracy $accuracy"
