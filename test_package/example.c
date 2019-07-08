/*
 * Copyright © 2012 inria.  All rights reserved.
 *
 * See COPYING in top-level directory
 *
 * $COPYRIGHT$
 *
 */

#include <xdrfile/xdrfile.h>

int main(int argc, char *argv[])
{
	XDRFILE * f = xdrfile_open("testfile.xdr", "w");//

    xdrfile_close(f);

    return 0;
}
