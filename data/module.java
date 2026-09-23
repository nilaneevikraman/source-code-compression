public class Module {
    public static int calculateTotal(int[] numbers) {
        int total = 0;

        for (int number : numbers) {
            total = total + number;
        }

        return total;
    }

    public static void main(String[] args) {
        int[] numbers = {10, 20, 30, 40};
        int result = calculateTotal(numbers);

        System.out.println("Total: " + result);
    }
}
