package uk.ac.cam.bms53.prejava.ex3;

public class ArrayLife {

    public static boolean getFromPackedLong(long packed, int position) {
        return ((packed >>> position) & 1) == 1;
    }

    public static void main(String[] args) throws java.io.IOException {
        int size = Integer.parseInt(args[0]);
        long initial = Long.decode(args[1]);
        boolean[][] world = new boolean[size][size];
        //place the long representation of the game board in the centre of "world"
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 8; j++) {
                world[i + size / 2 - 4][j + size / 2 - 4] = getFromPackedLong(initial, i * 8 + j);
            }
        }
        play(world);
    }

    public static boolean getCell(boolean[][] world, int col, int row) {
        if (row >= world.length || row < 0 || col >= world[row].length || col < 0)
        {
            return false;
        }
        return world[row][col];
    }

    public static void setCell(boolean[][] world, int col, int row, boolean newval) {
        if (row >= world.length || row < 0 || col >= world[row].length || col < 0) {
            return;
        }
        world[row][col] = newval;
    }

    public static void print(boolean[][] world) {
        System.out.println("-");
        for (int row = 0; row < world.length; row++) {
            for (int col = 0; col < world[row].length; col++) {
                System.out.print(getCell(world, col, row) ? "#" : "_");
            }
            System.out.println();
        }
    }

    public static int countNeighbours(boolean[][] world, int col, int row) {
        int num_neighbors = 0;
        // i and j are offsets to col; a neighbor can be any cell within +/-1 of the
        // cells col and row.
        for (int i = -1; i <= 1; i++) {
            for (int j = -1; j <= 1; j++) {
                // this boolean expression verifies that i and j are not both 0 (we aren't going to count the cell itself)
                // and then based on this (or the appropriate getCell call) we add to num_neighbors
                if (!(i == 0 && j == 0) && getCell(world, col + i, row + j))
                    num_neighbors++;
            }
        }
        return num_neighbors;
    }

    public static boolean computeCell(boolean[][] world, int col, int row) {
        int num_neighbors = countNeighbours(world, col, row);
        if (getCell(world, col, row)) {
            if (num_neighbors < 2)
                return false;
            else if (num_neighbors == 2 || num_neighbors == 3)
                return true;
            return false;
        } else {
            if (num_neighbors == 3)
                return true;
            return false;
        }
    }

    public static boolean[][] nextGeneration(boolean[][] world) {
        boolean[][] new_world = new boolean[world.length][world[0].length];
        for (int row = 0; row < world.length; row++) {
            for (int col = 0; col < world[row].length; col++)
                setCell(new_world, col, row, computeCell(world, col, row));
        }
        return new_world;
    }

    public static void play(boolean[][] world) throws java.io.IOException {
        int userResponse = 0;
        while (userResponse != 'q') {
            print(world);
            userResponse = System.in.read();
            world = nextGeneration(world);
        }
    }
}