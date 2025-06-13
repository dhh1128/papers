# Intent Boundaries
Daniel Hardman &mdash; 10 June 2025

<span class="hash">#ux #ssi #agents</span> 

<hr>

Yesterday I helped a visiting friend who was unfamiliar with the remote for our smart TV. While he sat on our couch, I quickly navigated the catalog of our streaming service, picked a show, and started viewing.

Five minutes later, I noticed an email from the content provider, thanking me for agreeing to an upgraded subscription. The content I had accessed required premium membership, and by beginning to stream, I had agreed to the terms, conditions, and a bigger monthly bill.

This was not my intent when I clicked the big blue "Watch" button that had focus in the UI.

Intent has been thoughtfully explored in various disciplines &mdash; notably, cybersecurity [[1](#n1), [2](#n2), [3](#n3), [4](#n4), [5](#n5)], human-computer action and UX theory [[6](#n6), [7](#n7), [3](#n3), [4](#n4), [5](#n5)], law and governance, and agentic AI. [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13] Unfortunately, more than three decades of experience designing and building software leads me to the conclusion that, while intent is often discussed and referenced informally, it is rarely modeled with sufficient rigor. We lack the ability to decide crucial questions, such as:

* How will we decide whether system behavior is aligned with user intent?
* How will we cope with misalignments to honor the principle of least surprise?
* What other stakeholders besides the direct user     

I therefore introduce some formal definitions and use them to build a conceptual framework that is relevant to user convenience, confidence, and safety in an age of powerful new agents.

## Endnotes

1. <a id="n1"></a>Saltzer, J.H. and Schroeder, M.D. 1975. The protection of information in computer systems. *Proceedings of the IEEE* 63, 9, 1278–1308.
   DOI: [10.1109/PROC.1975.9939](https://doi.org/10.1109/PROC.1975.9939)

2. <a id="n2"></a>Chandola, V., Banerjee, A., and Kumar, V. 2009. Anomaly detection: A survey. *ACM Computing Surveys* 41, 3, Article 15 (July 2009), 1–58.
   DOI: [10.1145/1541880.1541882](https://doi.org/10.1145/1541880.1541882)

3. <a id="n3"></a>Adams, A. and Sasse, M.A. 1999. Users are not the enemy. *Communications of the ACM* 42, 12, 40–46.
   DOI: [10.1145/322796.322806](https://doi.org/10.1145/322796.322806)

4. <a id="n4"></a>Pfleeger, S.L., Predd, J.B., Hunker, J., and Bulford, C. 2010. Insiders behaving badly: Addressing bad actors and their actions. *IEEE Transactions on Information Forensics and Security* 5, 1, 169–179.
   DOI: [10.1109/TIFS.2009.2039591](https://doi.org/10.1109/TIFS.2009.2039591)

5. <a id="n5"></a>Whitten, A. and Tygar, J.D. 1999. Why Johnny can't encrypt: A usability evaluation of PGP 5.0. In *Proceedings of the 8th USENIX Security Symposium*, 169–184.
    DOI: [10.5555/1251421.1251435]https://dl.acm.org/doi/10.5555/1251421.1251435)

6. <a id="n6"></a>Norman, D.A. 2013. *The Design of Everyday Things*. Revised and expanded edition. MIT Press.
   [https://mitpress.mit.edu/9780262525671/the-design-of-everyday-things/](https://mitpress.mit.edu/9780262525671/the-design-of-everyday-things/)

7. <a id="n7"></a>Suchman, L.A. 1987. *Plans and Situated Actions: The Problem of Human-Machine Communication*. Cambridge University Press.
   [https://www.jstor.org/stable/25469965](https://www.jstor.org/stable/25469965)

9. <a id="n9"></a>Shneiderman, B. 1983. Direct manipulation: A step beyond programming languages. *IEEE Computer* 16, 8 (Aug. 1983), 57–69.
   DOI: [10.1109/MC.1983.1654471](https://doi.org/10.1109/MC.1983.1654471)

10. <a id="n10"></a>Kaptelinin, V. and Nardi, B.A. 2006. *Acting with Technology: Activity Theory and Interaction Design*. MIT Press.
   [https://mitpress.mit.edu/9780262113111/acting-with-technology/](https://mitpress.mit.edu/9780262113111/acting-with-technology/)

11. <a id="n11"></a>Winograd, T. and Flores, F. 1986. *Understanding Computers and Cognition: A New Foundation for Design*. Ablex Publishing.
   Later reprinted by Addison-Wesley. No DOI available.
   [https://dl.acm.org/doi/book/10.5555/53730](https://dl.acm.org/doi/book/10.5555/53730)

12. <a id="n12"></a>Floridi, L. 2013. *The Ethics of Information*. Oxford University Press.
    [https://doi.org/10.1093/acprof\:oso/9780199551378.001.0001](https://doi.org/10.1093/acprof:oso/9780199551378.001.0001)

13. <a id="n13"></a>Nissenbaum, H. 2009. *Privacy in Context: Technology, Policy, and the Integrity of Social Life*. Stanford University Press.
    [https://www.sup.org/books/title/?id=8862](https://www.sup.org/books/title/?id=8862)

14. <a id="n14"></a>American Law Institute. 1962. *Model Penal Code: Official Draft and Explanatory Notes*. American Law Institute.
   [https://www.ali.org/publications/show/model-penal-code/](https://www.ali.org/publications/show/model-penal-code/)

15. <a id="n15"></a>République Française. *Code Civil (French Civil Code)*. Légifrance.
   [https://www.legifrance.gouv.fr/codes/id/LEGITEXT000006070721/](https://www.legifrance.gouv.fr/codes/id/LEGITEXT000006070721/)

16. <a id="n16"></a>Federal Ministry of Justice and Consumer Protection (Germany). *Strafgesetzbuch – German Criminal Code (English translation)*.
   [https://www.gesetze-im-internet.de/englisch\_stgb/](https://www.gesetze-im-internet.de/englisch_stgb/)

17. <a id="n17"></a>International Criminal Court. 1998. *Rome Statute of the International Criminal Court*. United Nations.
   [https://www.icc-cpi.int/sites/default/files/RS-Eng.pdf](https://www.icc-cpi.int/sites/default/files/RS-Eng.pdf)

18. <a id="n18"></a>United Nations. 1984. *Convention Against Torture and Other Cruel, Inhuman or Degrading Treatment or Punishment*.
   [https://www.ohchr.org/en/instruments-mechanisms/instruments/convention-against-torture-and-other-cruel-inhuman-or-degrading](https://www.ohchr.org/en/instruments-mechanisms/instruments/convention-against-torture-and-other-cruel-inhuman-or-degrading)

19. <a id="n19"></a>Ibn al-Ḥajjāj al-Muslim. ca. 9th century. *Ṣaḥīḥ Muslim*, Book 33, Hadith 4692. Translated by Abdul Hamid Siddiqui.
   Reference via: Sunnah.com.
   [https://sunnah.com/muslim:1907a](https://sunnah.com/muslim:1907a)

20. <a id="n20"></a>Babylonian Talmud. *Berakhot 13a*. The William Davidson Talmud via Sefaria.
   [https://www.sefaria.org/Berakhot.13a](https://www.sefaria.org/Berakhot.13a)

21. <a id="n20"></a>Brignull, H. "The Dark Patterns of UX Design." UX Design. Available at: https://www.darkpatterns.org (Accessed: June 2025).

22. <a id="n20"></a>Norwegian Consumer Council. 2018. Dark Patterns at Scale: Findings from a Study of 5,000 Mobile Apps. Norwegian Consumer Council. Available at: https://www.forbrukerradet.no/en/report/dark-patterns-at-scale/ (Accessed: June 2025).

23. <a id="n20"></a>Brignull, H. "Dark Patterns." UX Design, 2010. Available at: https://www.darkpatterns.org (Accessed: June 2025).

