bump $t0, $zero, 5000
bump $t1, $zero, 5004
bump $t2, $zero, 5008
bump $t3, $zero, 5012
bump $t4, $zero, 1
save $t4, 0($t1)
while_0:
grab $t5, 0($t1)
less $t7, $t5, $t6
less $t8, $t5, $t6
less $t9, $t6, $t5
dif $t8, $zero, $t8
bump $t8, $t8, 1
dif $t9, $zero, $t9
bump $t9, $t9, 1
conj $t8, $t8, $t9
disj $t7, $t7, $t8

when $t9, $zero, endwhile_0
grab $t10, 0($t1)
save $t10, 0($t2)
while_1:
grab $t11, 0($t2)
less $t13, $t12, $t11
less $t14, $t11, $t12
less $t15, $t12, $t11
dif $t14, $zero, $t14
bump $t14, $t14, 1
dif $t15, $zero, $t15
bump $t15, $t15, 1
conj $t14, $t14, $t15
disj $t13, $t13, $t14

when $t15, $zero, endwhile_1
grab $t16, 0($t2)
bump $t17, $zero, 3
dif $t18, $t16, $t17
save $t18, 0($t2)
skip $zero, $zero, while_1
endwhile_1:
grab $t19, 0($t1)
save $t19, 0($t3)
while_2:
grab $t20, 0($t3)
less $t22, $t21, $t20
less $t23, $t20, $t21
less $t24, $t21, $t20
dif $t23, $zero, $t23
bump $t23, $t23, 1
dif $t24, $zero, $t24
bump $t24, $t24, 1
conj $t23, $t23, $t24
disj $t22, $t22, $t23

when $t24, $zero, endwhile_2
grab $t25, 0($t3)
bump $t26, $zero, 5
dif $t27, $t25, $t26
save $t27, 0($t3)
skip $zero, $zero, while_2
endwhile_2:
grab $t28, 0($t2)
bump $t29, $zero, 0
less $t30, $t28, $t29
less $t31, $t29, $t28
dif $t30, $zero, $t30
bump $t30, $t30, 1
dif $t31, $zero, $t31
bump $t31, $t31, 1
conj $t30, $t30, $t31

skip $t31, $zero, else_3
grab $t32, 0($t3)
less $t34, $t32, $t33
less $t35, $t33, $t32
dif $t34, $zero, $t34
bump $t34, $t34, 1
dif $t35, $zero, $t35
bump $t35, $t35, 1
conj $t34, $t34, $t35

skip $t35, $zero, else_3
maro
endif_3:
rmd
ucl
fcb
grab $t36, 0($t1)
bump $t37, $zero, 1
sum $t38, $t36, $t37
save $t38, 0($t1)
