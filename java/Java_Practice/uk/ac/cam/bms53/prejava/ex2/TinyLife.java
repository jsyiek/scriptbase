package uk.ac.cam.bms53.prejava.ex2;

public class TinyLife
{
    public static void main(String[] args) throws java.io.IOException
    {
        play(Long.decode(args[0]));
    }

    public static boolean getCell(long world, int col, int row)
    {
        if (col >= 8  || col < 0 || row >= 8 || row < 0)
        {
            return false;
        }
        return ((world >> (8L * row + col)) & 1L) == 1L;
    }

    public static long setCell(long world, int col, int row, boolean newval)
    {
        if (col >= 8  || col < 0 || row >= 8 || row < 0)
        {
            return 0L;
        }
        return PackedLong.set(world, 8 * row + col, newval);
    }

    public static void print(long world)
    {
        System.out.println("-");
        for (int row = 0; row < 8; row++)
        {
            for (int col = 0; col < 8; col++)
            {
                System.out.print(getCell(world, col, row) ? "#" : "_");
            }
            System.out.println();
        }
    }

    public static int countNeighbours(long world, int col, int row)
    {
        int num_neighbors = 0;
        // i and j are offsets to col; a neighbor can be any cell within +/-1 of the
        // cells col and row.
        for (int i = -1; i <= 1; i++)
        {
            for (int j = -1; j <= 1; j++)
            {
                // this boolean expression verifies that i and j are not both 0 (we aren't going to count the cell itself)
                // and then based on this (or the appropriate getCell call) we add to num_neighbors
                if (!(i == 0 && j == 0) && getCell(world, col + i, row + j))
                    num_neighbors++;
            }
        }
        return num_neighbors;
    }

    public static boolean computeCell(long world, int col, int row)
    {
        int num_neighbors = countNeighbours(world, col, row);
        if (getCell(world, col, row))
        {
            if (num_neighbors < 2)
                return false;
            else if (num_neighbors == 2 || num_neighbors == 3)
                return true;
            return false;
        }
        else
        {
            if (num_neighbors == 3)
                return true;
            return false;
        }
    }

    public static long nextGeneration(long world)
    {
        long new_world = 0L;
        for (int col = 0; col < 8; col++)
        {
            for (int row = 0; row < 8; row++)
                new_world = setCell(new_world, col, row, computeCell(world, col, row));
        }
        return new_world;
    }

    public static void play(long world) throws java.io.IOException {
        int userResponse = 0;
        while (userResponse != 'q') {
            print(world);
            userResponse = System.in.read();
            world = nextGeneration(world);
        }
    }
}