#include <stdio.h>

int main() {
	long a = 0, b = 0, c = 0, d = 0, e = 0, f = 0, g = 0, h = 0;
	b = 57, c = 57;
	a = 0;
	if (a != 1) {
		b *= 100;
		b -= -100000;
		c = b;
		c -= -17000;
	}

	while (1) {
		f = 1;
		d = 2;
		do {
			e = 2;

			// Since b and d are integers, if this isn't true, d * e will never equal b
			if (b % d == 0) {
				do {
					if (d * e == b) {
						f = 0;
					}
					e -= -1;
					g = e - b;
				} while (g != 0);
			}
			d -= -1;
			g = d - b;
		} while (g != 0);
		if (f == 0) {
			h -= -1;
		}
		g = b - c;
		if (g == 0) {
			break;
		}
		b -= -17;
	}

	printf("h: %d\n", h);
}
