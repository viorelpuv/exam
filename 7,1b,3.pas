PROGRAM BubbleSort(INPUT, OUTPUT);
VAR
  Sorted, Ch1, Ch2: CHAR;
  F1, F2: TEXT;
BEGIN {BubbleSort}
  Sorted := 'N';
  REWRITE(F1);
  WHILE NOT EOLN(INPUT)
  DO
    BEGIN
      READ(INPUT, Ch1);
      WRITE(F1, Ch1);
    END;
  WRITELN(F1);
  WHILE Sorted = 'N'
  DO
    BEGIN
      Sorted := 'Y';
      RESET(F1);
      REWRITE(F2);    
      IF NOT EOLN(F1)
      THEN
        BEGIN
          READ(F1, Ch1);
          WHILE NOT EOLN(F1)
          DO
            BEGIN
              READ(F1, Ch2);
              IF Ch1 <= Ch2
              THEN
                BEGIN
                  WRITE(F2, Ch1);
                  Ch1 := Ch2
                END 
              ELSE
                BEGIN
                  WRITE(F2, Ch2);
                  Sorted := 'N'
                END;
            END;     
          WRITE(F2, Ch1);
        END;
      WRITELN(F2); 
      RESET(F2);
      REWRITE(F1);
      WHILE NOT EOLN(F2)
      DO
        BEGIN
          READ(F2, Ch1);
          WRITE(F1, Ch1);
        END;
      WRITELN(F1);
    END;
  RESET(F1);
  WHILE NOT EOLN(F1)
  DO
    BEGIN
      READ(F1, Ch1);
      WRITE(OUTPUT, Ch1);
    END;
  WRITELN(OUTPUT);
END. {BubbleSort}

