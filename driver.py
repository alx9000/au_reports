#!/home/common/scripts/python/bin/python3

import rota
import sys


r_head = '{:s} breakdown for {:s}/{:s} w/c: {:s}/{:s}/{:s}'
sec_head = '{:s} - {:s}: {:.1f} lines'
t_head = ' |-->{:.<15s}' + '{:.>4s}' + '{:>4s}'*6 + ' |{:>5s}'
t_body = ' |-->{:.<15s}' + '{:.>4d}' + '{:>4d}'*6 + ' |{:5d}'

def books(R):
    
    print('Breakdown for ',garage,': w/c ',date)
    for book,duties in sorted(R.by_book().items()):
        print(t_body.format(book,*duties,sum(duties)))
    print('-'*54)
    print(t_body.format('TOTALS',*R.requirement(),sum(R.requirement())))
    print('='*54)

def sectiondata(R):
    print(r_head.format('Section',R.garage,R.draft,R.date['day'],R.date['mth'],R.date['year'])) 
    for sec in R.sections:
        print(sec_head.format(sec.Id,sec.name,sum(sec.requirement())/5))
        print(t_head.format('Book','Sa','Su','Mo','Tu','We','Th','Fr','Tot'))
        for book,duties in sorted(sec.by_book().items()):
            print(t_body.format(book,*duties,sum(duties)))
        print('','-'*54)
        print(t_body.format('Total',*sec.requirement(),sum(sec.requirement())))
        print(t_body.format('Spares',*sec.spares,sum(sec.spares)))
        print('','='*54)
    

try:
    command = sys.argv[1]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} COMMAND")

if command == 'books':
    try:
        garage = sys.argv[2].upper()
        date = sys.argv[3].replace('/','')
        dset = sys.argv[4]
        R = rota.Rota(garage,date)
        books(R)

    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} books GARAGE dd/mm/yyyy DATASET")
    except FileNotFoundError:
        raise SystemExit(f"{sys.argv[0]}: could not find rota for {garage} commencing {date} in dataset {dset}")

elif command == 'sections':
    try:
        garage = sys.argv[2].upper()
        date = sys.argv[3].replace('/','')
        dset = sys.argv[4]
        R = rota.Rota(garage,date)
        sectiondata(R)
    except IndexError:
        raise SystemExit(f"Usage: {sys.argv[0]} sections GARAGE dd/mm/yyyy DATASET")
    except FileNotFoundError:
        raise SystemExit(f"{sys.argv[0]}: could not find rota for {garage} commencing {date} in dataset {dset}")

