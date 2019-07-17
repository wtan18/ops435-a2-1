#!/usr/bin/env python3
# author: Raymond Chan
# date: February, 2018
#

import time


def normalized_rec(rec):
    '''Normalize login record produced by the last command.
       The login and logout time could be or not be on the same day.
       eg: (1) Mon Jan 01 12:23:34 2018 - Mon Jan 01 22:11:00 2018 
       or  (2) Mon Jan 01 23:10:45 2018 - Tue Jan 02 00:15:43 2018
       or  (3) Mon Jan 01 09:00:23 2018 - Fri Jan 05 17:00:07 2018
       The login and logout time for (1) are on the same day, this 
       record does not need to be normalized.
       The login and logout time for (2) are on two different days,
       after normalization, two records will be generated:
           (a) Mon Jan 01 23:10:45 2018 - Mon Jan 01 23:59:59 2018
           (b) Tue Jan 02 00:00:00 2018 - Tue Jan 02 00:15:43 2018

       The login and logout time for (2) spawn 5 days, after
       normalization, 5 records will be generated:
           (a) Mon Jan 01 09:00:23 2018 - Mon Jan 01 23:59:59 2018
           (b) Tue Jan 02 00:00:00 2018 - Tue Jan 02 23:59:59 2018
           (c) Wed Jan 03 00:00:00 2018 - Wed Jan 03 23:59:59 2018
           (d) Thu Jan 04 00:00:00 2018 - Thu Jan 04 23:59:59 2018
           (e) Fri Jan 05 00:00:00 2018 - Fri Jan 05 17:00:07 2018

          same day -> retrun the same record
          different days: 1st record -> keep login date/time
                                        change logout date 
                                        (update fields 9,10,11,12) 
                                        logout time-> 23:59:59
                          2nd record -> login day  +1 (update fields 3,4,5,7)
                                        time -> 00:00:00
                                        keep logout date/time
          pass the 2nd record to the normalized_rec function again
          Please note that this is a recursive function.
    ''' 
    jday = time.strftime('%j',time.strptime(' '.join(rec[4:6]+rec[7:8]),'%b %d %Y'))
    jday2 = time.strftime('%j',time.strptime(' '.join(rec[10:12]+rec[13:14]), '%b %d %Y'))
    if jday == jday2:
       norm_rec = []
       norm_rec.append(rec.copy())
       return norm_rec
    else:
       # calculate next day string in 'WoD Month Day HH:MM:SS YYYY'
       new_rec1 = rec.copy()
       new_rec = rec.copy()
       t_next = time.mktime(time.strptime(' '.join(new_rec1[4:6]+rec[7:8]),'%b %d %Y'))+86400
       next_day = time.strftime('%a %b %d %H:%M:%S %Y',time.strptime(time.ctime(t_next))).split()
       new_rec1[12] = '23:59:59'
       new_rec1[9] = new_rec1[3]
       new_rec1[10] = new_rec1[4]
       new_rec1[11] = new_rec1[5]
       new_rec[3] = next_day[0] # Day of week Sun, Mon, Tue...
       new_rec[4] = next_day[1] # Month Jan, Feb, Mar, ...
       new_rec[5] = next_day[2] # Day of Month 01, 02, ...
       new_rec[6] = next_day[3] # Time HH:MM:SS
       new_rec[7] = next_day[4] # Year YYYY
       norm_rec = normalized_rec(new_rec)
       normalized_recs = norm_rec.copy()
       normalized_recs.insert(0,new_rec1)  # call normalized_rec function recursive
    return normalized_recs

def diurnal(rec):
    '''non-recursive way to normalized login records'''
    norm_rec = []
    login_day = ' '.join(rec[4:6]+rec[7:8])
    logout_day = ' '.join(rec[10:12]+rec[13:14])
    day_format = '%b %d %Y'
    sec_t_in = time.mktime(time.strptime(login_day,day_format))
    sec_t_out = time.mktime(time.strptime(logout_day,day_format))

    n_day = int((sec_t_out - sec_t_in)/86400)
    if n_day == 0:
       norm_rec.append(rec.copy())
    else:
       rec1 = rec.copy()
       rec1[12] = '23:59:59'
       rec1[9] = rec1[3]
       rec1[10] = rec1[4]
       rec1[11] = rec1[5]
       norm_rec.append(rec1.copy())
       for x in range(n_day):
           new_rec = rec.copy()
           t_next = sec_t_in + (x+1)*86400
           next_day = time.strftime('%a %b %d %H:%M:%S %Y', time.strptime(time.ctime(t_next))).split()
           new_rec[3] = next_day[0]
           new_rec[4] = next_day[1]
           new_rec[5] = next_day[2]
           new_rec[6] = next_day[3]
           new_rec[7] = next_day[4]
           if (x+1) != n_day:
               new_rec[12] = '23:59:59'
               new_rec[9] = new_rec[3]
               new_rec[10] = new_rec[4]
               new_rec[11] = new_rec[5]
               new_rec[13] = new_rec[7]
           norm_rec.append(new_rec.copy())
    return norm_rec


