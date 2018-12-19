#include <assert.h>
#include <stdio.h>

int main() {
	long long r0 = 1, r1 = 0, r2 = 0 /* ip */, r3 = 0, r4 = 0, r5 = 0;

l0:
	r2 += 16; // addi 2 16 2
	goto l17;
l1:
	r3 = 1; // seti 1 4 3
l2:
	r1 = 1; // seti 1 5 1
l3:
	r5 = r3 * r1; // mulr 3 1 5
l4:
	r5 = r5 == r4 ? 1 : 0; // eqrr 5 4 5
l5:
	r2 = r5 + r2; // addr 5 2 2
	if (r5) goto l7;
l6:
	r2 = r2 + 1; // addi 2 1 2
	goto l8;
l7:
	r0 = r3 + r0; // addr 3 0 0
	if (r3) {
		printf("%ld, %ld, %ld, %ld, %ld, %ld\n", r0, r1, r2, r3, r4, r5);
	}
l8:
	r1 = r1 + 1; // addi 1 1 1
l9:
	r5 = r1 > r4 ? 1 : 0; // gtrr 1 4 5
l10:
	r2 = r2 + r5; // addr 2 5 2
	if (r5) goto l12;
l11:
	r2 = 2; // seti 2 9 2
	goto l3;
l12:
	r3 = r3 + 1; // addi 3 1 3
l13:
	r5 = r3 > r4 ? 1 : 0; // gtrr 3 4 5
l14:
	r2 = r5 + r2; // addr 5 2 2
	//printf("%ld, %ld, %ld, %ld, %ld, %ld\n", r0, r1, r2, r3, r4, r5);
	if (r5) goto l16;
l15:
	r2 = 1; // seti 1 6 2
	goto l2;
l16:
	r2 = r2 * r2; // mulr 2 2 2
	printf("%ld, %ld, %ld, %ld, %ld, %ld\n", r0, r1, r2, r3, r4, r5);
	goto l36;
l17:
	r4 = r4 + 2; // addi 4 2 4
	r4 = r4 * r4; // mulr 4 4 4
l19:
	//r4 = r2 * r4; // mulr 2 4 4
	r4 = 19 * r4; // mulr 2 4 4
l20:
	r4 = r4 * 11; // muli 4 11 4
	r5 = r5 + 7; // addi 5 7 5
l22:
	//r5 = r5 * r2; // mulr 5 2 5
	r5 = r5 * 22; // mulr 5 2 5
l23:
	r5 = r5 + 4; // addi 5 4 5
	r4 = r4 + r5; // addr 4 5 4
l25:
	//r2 = r2 + r0; // addr 2 0 2
	if (r0 == 1) goto l27;
	assert(r0 == 0);
l26:
	r2 = 0; // seti 0 1 2
	goto l1;
l27:
	//r5 = r2 + r1; // setr 2 1 5
	r5 = 27 + r1; // setr 2 1 5
l28:
	//r5 = r5 * r2; // mulr 5 2 5
	r5 = r5 * 28; // mulr 5 2 5
l29:
	//r5 = r2 + r5; // addr 2 5 5
	r5 = 29 + r5; // addr 2 5 5
l30:
	//r5 = r2 * r5; // mulr 2 5 5
	r5 = 30 * r5; // mulr 2 5 5
l31:
	r5 = r5 * 14; // muli 5 14 5
l32:
	//r5 = r5 * r2; // mulr 5 2 5
	r5 = r5 * 32; // mulr 5 2 5
l33:
	r4 = r4 + r5; // addr 4 5 4
l34:
	r0 = 0; // seti 0 6 0

l35:
	r2 = 0; // seti 0 6 2
	goto l1;

l36:
	printf("%ld, %ld, %ld, %ld, %ld, %ld\n", r0, r1, r2, r3, r4, r5);
}
