for i in {1..5}
do
   screen -dmS screen$i bash -c 'python ~/stabilityaixl/backend/websocket/client.py; exec sh'
done