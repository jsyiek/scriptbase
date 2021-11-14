package uk.ac.cam.bms53.prejava.demo;

class Reference {
    public static void update(int i, int[] array) {
        i++;
        array[0]++;
    }

    public static void main(String[] args) {
        int test_i = 1;
        int[] test_array = {1};

        update(test_i, test_array);

        System.out.println(test_i);
        System.out.println(test_array[0]);
    }
}