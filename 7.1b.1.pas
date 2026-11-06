PROGRAM BubbleSort(INPUT, OUTPUT);
VAR
  Sorted, Ch1, Ch2: CHAR;
  F1, F2: TEXT;
BEGIN{BubbleSort}
  Sorted := 'N';
  REWRITE(F1);
  WHILE NOT EOLN(INPUT)
  DO
    BEGIN
      READ(INPUT, Ch1);
      WRITE(F1, Ch1);
    END;
  WHILE Sorted = 'N'
  DO
    BEGIN
      Sorted := 'Y'
     {Копируем F1 в F2,проверяя отсортированностьи переставляя первые соседние символы по порядку}
     {Копируем F2 в F1}
    END;
  WRITELN(F1);
  RESET(F1);
  WHILE NOT EOLN(F1)
  DO
    BEGIN
      READ(F1, Ch1);
      WRITE(OUTPUT, Ch1);
    END;
  WRITELN(OUTPUT)
END.{BubbleSort}

