## Installation

1. Make sure [Python 3.6+](https://www.python.org/downloads/) is installed along with pip.


2. Install [pipenv](https://github.com/kennethreitz/pipenv) and requirements ( dependancies )


```
$ pip install pipenv ( ή sudo -H pip3 install -U pipenv σε ubuntu)


pipenv --python [path/to/python3/executable] ( σε ubuntu 16.04 ενδέχεται να χρειαστεί)


pipenv install flask ( αν  εμφανιστεί μήνυμα κατά την εκτέλεση )
```

3. Run the server and the cli:
    * `$ pipenv run python api.py -p [port_number] -a [admins_port_number] -l [last_digit_of_ip]`

   where admins_port_number==port_number only for the admin and last digit goes from 1 ( admin ) to 5 ( for 5 nodes)

   e.g for 5 nodes:
      * `$ pipenv run python3.7 api.py -p 5000 -a 5000 -l 1`
      * `$ pipenv run python3.7 api.py -p 5001 -a 5000 -l 2`
      * `$ pipenv run python3.7 api.py -p 5001 -a 5000 -l 3`
      * `$ pipenv run python3.7 api.py -p 5001 -a 5000 -l 4`
      * `$ pipenv run python3.7 api.py -p 5001 -a 5000 -l 5`

   In the above example , the first node is the admin  with  local ip address : 192.168.0.1

4.Run the cli:

    * $ pipenv run python cli.py port_number last_digit_of_ip {port}


   e.g for 5 nodes:


      * `$ pipenv run python3.7 cli.py  1 5000`
      * `$ pipenv run python3.7 cli.py  2 5001`
      * `$ pipenv run python3.7 cli.py  3 5001`
      * `$ pipenv run python3.7 cli.py  4 5001`
      * `$ pipenv run python3.7 cli.py  5 5001`

 Note that the "python3.7" can be 3.6 depending on the python's version  installed on each computer.
