# Guess-the-number

Aplicație de tip server - client care va reproduce jocul Ghicește Numărul. Numărul ce trebuie ghicit se va afla în intervalul [0, 50]. Vor exista 2 posibilități: fie numărul va fi generat de server, fie va fi dat de către un alt client - în situația în care vor să joace 2 persoane. La fiecare încercare de a ghici numărul, clientul va primi unul din mesajele : numărul este corect / numărul este mai mic / mai mare decât numărul ales. Fiecare rulare a scriptului va reprezenta o sesiune de joc, formată din mai multe partide de joc. La finalul sesiunii, se va afișa scorul maxim – care va reprezenta cel mai mic număr de încercări necesar descoperirii numărului.

INPUT: server.py
client1.py (care trimite un număr sau nu)
client2.py (este clientul care trimite câte un număr catre server, orice decizie luată de server fiind afișată ambilor participanți – ex. Client 1 ghiceste -> notificați ambii participanți că jocul s-a terminat, cu Scorul și Scorul Maxim aferent)

OUTPUT: 
