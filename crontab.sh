if [ -f ~/.bashrc ]; then
    . ~/.bashrc

fi
((
    cd ~/connecting_box/ && \
    python3 ./contents/crontab_rescue.py
) > ~/log/crontab_rescue.log 2>&1)