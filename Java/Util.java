import java.util.Scanner;

public class Util
{
    public static int getChoice(String[] options, String prompt)
    {
        Scanner input = new Scanner(System.in);
        String choice;
        int choiceInt;
        
        while(true)
        {
            for(int i = 0; i < options.length; i++)
            {
                System.out.println((i + 1) + ". " + options[i]);
            }

            System.out.print(">>> ");
            choice = input.nextLine();

            try
            {
                choiceInt = Integer.valueOf(choice);

                if(choiceInt > 0 && choiceInt <= options.length)
                {
                    return choiceInt;
                }

                else
                {
                    System.out.println("That's not one of the choices.");
                }
            }

            catch(Exception e)
            {
                System.out.println("Please enter a number.");
            }
        }
    }

    public static double getNumber(String prompt, double bound, boolean requirePositive)
    {
        Scanner input = new Scanner(System.in);
        String choice;
        double choiceDouble;

        while(true)
        {
            System.out.println("\n" + prompt);

            try
            {
                choiceDouble = Double.valueOf(choice);

                if(bound != 0 && choiceDouble > bound)
                {
                    System.out.println("That value is too high.");
                }

                else if(requirePositive && choiceDouble < 0)
                {
                    System.out.println("Your input must be positive.");
                }

                else
                {
                    return choiceDouble;
                }
            }

            catch(Exception e)
            {
                System.out.println("Please enter a number.");
                
            }
        }
    }
}
