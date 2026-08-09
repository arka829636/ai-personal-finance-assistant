from ai_advisor import generate_advice

from transactions import (
    add_transaction,
    show_transactions
)

from analysis import (
    show_summary,
    monthly_analysis,
    financial_insights
)

from budget import budget_analysis

from finance_chat import finance_chat

from recommendations import generate_recommendations


def main():

    while True:

        print("\n===== AI PERSONAL FINANCE ASSISTANT =====")

        print("1. Add Transaction")
        print("2. Show Financial Summary")
        print("3. Show All Transactions")
        print("4. Monthly Analysis")
        print("5. Financial Insights")
        print("6. Budget Analysis")
        print("7. AI Financial Advisor")
        print("8. Finance Chat Assistant")
        print("9. Financial Recommendations")
        print("10. Exit")

        choice = input("\nEnter your choice: ")

        # --------------------------------
        # ADD TRANSACTION
        # --------------------------------

        if choice == "1":

            add_transaction()

        # --------------------------------
        # FINANCIAL SUMMARY
        # --------------------------------

        elif choice == "2":

            show_summary()

        # --------------------------------
        # SHOW ALL TRANSACTIONS
        # --------------------------------

        elif choice == "3":

            show_transactions()

        # --------------------------------
        # MONTHLY ANALYSIS
        # --------------------------------

        elif choice == "4":

            monthly_analysis()

        # --------------------------------
        # FINANCIAL INSIGHTS
        # --------------------------------

        elif choice == "5":

            financial_insights()

        # --------------------------------
        # BUDGET ANALYSIS
        # --------------------------------

        elif choice == "6":

            budget_analysis()

        # --------------------------------
        # AI FINANCIAL ADVISOR
        # --------------------------------

        elif choice == "7":

            generate_advice()

        # --------------------------------
        # FINANCE CHAT ASSISTANT
        # --------------------------------

        elif choice == "8":

            finance_chat()

        # --------------------------------
        # FINANCIAL RECOMMENDATIONS
        # --------------------------------

        elif choice == "9":

            generate_recommendations()

        # --------------------------------
        # EXIT
        # --------------------------------

        elif choice == "10":

            print(
                "\nThank you for using "
                "AI Personal Finance Assistant!"
            )

            print("Goodbye! 👋")

            break

        # --------------------------------
        # INVALID CHOICE
        # --------------------------------

        else:

            print(
                "\n❌ Invalid choice. "
                "Please enter a number from 1 to 10."
            )


if __name__ == "__main__":

    main()