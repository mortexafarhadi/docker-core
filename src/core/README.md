
# Core (Basic Django Project)
Step-by-Step Guide to Building New Project

(with Base Setting)
## Deployment

Step 1 ( Clone Project )

```bash
  git clone https://github.com/mortexafarhadi/core.git
```

Step 2 ( change SECRET_KEY )

```bash
  generate new secret key ( example -> https://djecrety.ir/)
  copy .env-sample to .env file
  set new data for SECRET_KEY and other variable (in .env file) 
```

Step 3 ( Create virtualenv (venv) )

```bash
  PyCharm          ->    Add New Interpreter

  VSCode (or cmd)  ->    py -m virtualenv venv
```

Step 4 ( Active venv )

```bash
  PyCharm          ->    restart IDE

  VSCode (or cmd)  ->    *windows:   venv\Script\activate
                         *linux  :   source venv\bin\activate
```

Step 5 ( Install External Packages )

```bash
  pip install -r zzrequirements/development.txt
```
Step 6 ( Create and Migrate Datebase )

```bash
  I-  python manage.py makemigrations
  II- python manage.py migrate
```
Step 7 ( Test Server )

```bash
  PyCharm          ->    run project

  VSCode (or cmd)  ->    python manage.py runserver
```

Step 8 ( Create Blank Project in Git )

    github.com  ->  repository/new -> blank project
    gitlab.com  ->  projects/new  ->  blank project


Step 9 ( Change Project Setting on Git )
    
    gitlab
        project-name  ->  Settings  ->  Repository  ->
        Protected branches  ->  Allowed to force push  ->  Ture


Step 10 ( Git Reset url Remote to Your Project and Check)

```bash
  I-      copy git link -> https://github.com/mortexafarhadi/your-repository.git
  II-     git remote set-url origin https://github.com/mortexafarhadi/your-repository.git
  III-    git remote -v
```


Step 11 ( Push Your Project to Git )

```bash
  git push
  -- or --
  git push -uf origin main
```


Enjoy It.
## Author

- [@mortexafarhadi](https://gitlab.com/mortexafarhadi)

