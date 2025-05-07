int i;
int mod3;
int mod5;

i = 1;
while (i <= 100) {
    mod3 = i;
    while (mod3 >= 3) {
        mod3 = mod3 - 3;
    }
    
    mod5 = i;
    while (mod5 >= 5) {
        mod5 = mod5 - 5;
    }
    
    if (mod3 == 0 && mod5 == 0) {
        printf("FizzBuzz\n");
    } else if (mod3 == 0) {
        printf("Fizz\n");
    } else if (mod5 == 0) {
        printf("Buzz\n");
    } else {
        printf("%d\n", i);
    }
    
    i = i + 1;
}

return 0;