#!/usr/bin/env python

import time

def recv_timeout(s,timeout=2):
    s.setblocking(0)
    total_data=[];
    data='';
    begin=time.time()
    while True:
        if total_data and time.time()-begin > timeout:
            break
        elif time.time()-begin > timeout*2:
            break
        try:
            data = s.recv(8192)
            if data:
                total_data.append(data)
                begin=time.time()
            else:
                time.sleep(0.1)
        except Exception:
            time.sleep(0.1)
    return ''.join(total_data)
