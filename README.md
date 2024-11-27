# Assignment2
## Group Members
1. Aakanksha Pharande
2. Vrinda Dua
3. Talwinder Singh (040952048)

## Scenario Description:
The Rideau Canal Skateway is one of the world's largest natural ice skating venues, attracting thousands of visitors each winter. To ensure the safety of skaters, continuous monitoring of ice and weather conditions is crucial. Dynamic factors like ice thickness, surface temperature, and snow accumulation can rapidly change, making it essential to assess these metrics in real time to determine if the Skateway is safe for public use.
### How it solves the problem:
This project deploys simulated IoT sensors at three key locations along the Rideau Canal: Dow's Lake, Fifth Avenue, and the NAC. These sensors provide live updates on critical parameters, including:

Ice Thickness: Ensures the ice meets safety standards for skating.
Surface Temperature: Detects early signs of ice melting risks.
Snow Accumulation: Assesses the impact of snow on ice stability.
External Temperature: Provides context for overall weather conditions.
The collected data is processed in real time using Azure Stream Analytics and stored in Azure Blob Storage. This real-time processing enables the National Capital Commission (NCC) to identify hazards quickly, take immediate action, and maintain a safe environment for skaters. Additionally, the stored data offers valuable insights for historical analysis, helping to improve long-term safety and maintenance protocols.

By leveraging continuous monitoring and data-driven decision-making, this solution enhances the safety and reliability of the Rideau Canal Skateway for everyone.
