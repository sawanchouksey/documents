## 🚀 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐧𝐠 𝐊𝐮𝐛𝐞𝐫𝐧𝐞𝐭𝐞𝐬 𝐇𝐏𝐀 𝐌𝐚𝐧𝐚𝐠𝐞𝐦𝐞𝐧𝐭 𝐰𝐢𝐭𝐡 𝐚 𝐂𝐮𝐬𝐭𝐨𝐦 𝐒𝐜𝐫𝐢𝐩𝐭 🖥️

##### 𝗦𝗰𝗿𝗶𝗽𝘁 𝘀𝗻𝗶𝗽𝗽𝗲𝘁:

```
#!/bin/bash

# Get all HPAs across all namespaces
HPA_LIST=$(kubectl get hpa -A --no-headers)

while read -r line; do
    # Extract namespace, name, current replicas, and max replicas
    NAMESPACE=$(echo $line | awk '{print $1}')
    HPA_NAME=$(echo $line | awk '{print $2}')
    HPA_STATUS=$(kubectl get hpa ${HPA_NAME} -n ${NAMESPACE} -o custom-columns=CURRENT:.status.currentReplicas,DESIRED:.spec.maxReplicas --no-headers)
    CURRENT_REPLICAS=$(echo $HPA_STATUS | awk '{print $1}')
    DESIRED_REPLICAS=$(echo $HPA_STATUS | awk '{print $2}')
    if [ $DESIRED_REPLICAS -gt 7 ]; then
        # Check if current replicas is one less than desired replicas
        if [ $CURRENT_REPLICAS -eq $((DESIRED_REPLICAS - 2)) ]; then
            echo "HPA $HPA_NAME in namespace $NAMESPACE:"
            echo "Current replicas ($CURRENT_REPLICAS) is one less than desired replicas ($DESIRED_REPLICAS). Increasing desired replicas by 2."

            # Calculate new desired replica count
            NEW_DESIRED_REPLICAS=$((DESIRED_REPLICAS + 2))

            # Update the HPA
            kubectl patch hpa $HPA_NAME -n $NAMESPACE --patch "{\"spec\":{\"maxReplicas\":$NEW_DESIRED_REPLICAS}}"

            echo "Updated HPA to have $NEW_DESIRED_REPLICAS max replicas."
            echo "------------------------"
        else
            echo "HPA $HPA_NAME in namespace $NAMESPACE:"
            echo "No action needed. Current replicas: $CURRENT_REPLICAS, Desired replicas: $DESIRED_REPLICAS"
            echo "------------------------"
        fi
    else
        echo "HPA $HPA_NAME in namespace $NAMESPACE:"
        echo "Desired replicas ($DESIRED_REPLICAS) is not greater than 5.
        if [ $CURRENT_REPLICAS -eq $((DESIRED_REPLICAS - 1)) ]; then
            echo "HPA $HPA_NAME in namespace $NAMESPACE:"
            echo "Current replicas ($CURRENT_REPLICAS) is one less than desired replicas ($DESIRED_REPLICAS). Increasing desired replicas by 2."

            # Calculate new desired replica count
            NEW_DESIRED_REPLICAS=$((DESIRED_REPLICAS + 2))

            # Update the HPA
            kubectl patch hpa $HPA_NAME -n $NAMESPACE --patch "{\"spec\":{\"maxReplicas\":$NEW_DESIRED_REPLICAS}}"

            echo "Updated HPA to have $NEW_DESIRED_REPLICAS max replicas."
            echo "------------------------"
        else
            echo "HPA $HPA_NAME in namespace $NAMESPACE:"
            echo "No action needed. Current replicas: $CURRENT_REPLICAS, Desired replicas: $DESIRED_REPLICAS"
            echo "------------------------"
        fi
    fi
done <<< "$HPA_LIST"
```

##### 𝗧𝗼 𝗶𝗺𝗽𝗹𝗲𝗺𝗲𝗻𝘁:

1. Ensure that the user running this cron job has the necessary permissions to execute kubectl commands.

2. Make the script executable:
   
   ```bash
   𝗰𝗵𝗺𝗼𝗱 +𝘅 /𝗵𝗼𝗺𝗲/𝗮𝘄𝘀𝘂𝘀𝗲𝗿/𝘂𝗽𝗱𝗮𝘁𝗲_𝗮𝗹𝗹_𝗵𝗽𝗮𝘀.𝘀𝗵
   ```

3. Open your crontab file for editing:
   
   ```bash
   𝗰𝗿𝗼𝗻𝘁𝗮𝗯 -𝗲
   ```

4. Add the following line to run the script every 10 minutes
   
   ```
   */𝟭𝟬 * * * * /𝗵𝗼𝗺𝗲/𝗮𝘄𝘀𝘂𝘀𝗲𝗿/𝘂𝗽𝗱𝗮𝘁𝗲_𝗮𝗹𝗹_𝗵𝗽𝗮𝘀.𝘀𝗵 >> /𝘃𝗮𝗿/𝗹𝗼𝗴/𝗵𝗽𝗮_𝘂𝗽𝗱𝗮𝘁𝗲.𝗹𝗼𝗴 𝟮>&𝟭
   ```

5. To check if the cron job is set up correctly, you can list your cron jobs:
   
   ```bash
   𝗰𝗿𝗼𝗻𝘁𝗮𝗯 -𝗹
   ```

6. To view the logs and check if the script is running as expected, you can tail the log file
   
   ```bash
   𝘁𝗮𝗶𝗹 -𝗳 /𝘃𝗮𝗿/𝗹𝗼𝗴/𝗵𝗽𝗮_𝘂𝗽𝗱𝗮𝘁𝗲.𝗹𝗼𝗴 𝟮>&𝟭
   ```

### Support Me

**If you find my content useful or enjoy what I do, you can support me by buying me a coffee. Your support helps keep this website running and encourages me to create more content.**

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sawanchokso)

**Your generosity is greatly appreciated!**
