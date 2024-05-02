# vendor management

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/harish-work/vendor_management.git
$ cd vendor_management
```

Create a virtual environment to install dependencies in and activate it:
```sh
$ virtualenv vendor-env
$ source env/bin/activate
```
Then install the dependencies:
```sh
(vendor-env)$ pip install -r requirements.txt
```
## Getting Started
```sh
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```
## Screenshots
1. Get Vendor performance.
2. !note to pass the token the header.
![performance](https://github.com/harish-work/vendor_management/assets/163814679/af5c246e-6e74-442c-a108-b1bfd45939b3)

2.Get all vendors list details.
![all_vendor](https://github.com/harish-work/vendor_management/assets/163814679/3783e73b-3c3d-4980-89b5-d13dc3499019)

3.Get all purchase order list.
![all_po](https://github.com/harish-work/vendor_management/assets/163814679/6b3261dc-9dd4-4ebd-9519-669ed3cc5a9d)



