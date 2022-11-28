package tools;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;

public class AppendDatasetByCopy {

  /**
   * cd /home/fit/dataset_zhongyan/apache-iotdb-0.10.1/tools cp select/* /disk/yanchang_dataset/.
   * for element in `ls select/$1` do java VLDBExpCopyNine select/$element
   * /disk/yanchang_dataset/$element done
   */

  public static void main(String[] args) throws IOException {
    String file = args[0];
    String extendedFile = args[1]; // empty
    int copyNum = Integer.parseInt(args[2]);
    String csvSplitBy = ",";
    PrintWriter writer = new PrintWriter(new FileOutputStream(new File(extendedFile), true));
    // 获取时间偏移量T=最后一个点+(第二个点-第一个点)-第一个点
    String line;
    String firstRow = null;
    String secondRow = null;
    String lastRow = null;
    BufferedReader readerInitial = new BufferedReader(new FileReader(file));
    System.out.println("skip header");
    readerInitial.readLine(); // skip header
    System.out.println("copy 1");
    firstRow = readerInitial.readLine();
    writer.println(firstRow);
    secondRow = readerInitial.readLine();
    writer.println(secondRow);
    while ((line = readerInitial.readLine()) != null) {
      lastRow = line;
      writer.println(line);
    }
    readerInitial.close();
    long firstTimestamp = Long.parseLong(firstRow.split(csvSplitBy)[0]);
    long secondTimestamp = Long.parseLong(secondRow.split(csvSplitBy)[0]);
    long lastTimestamp = Long.parseLong(lastRow.split(csvSplitBy)[0]);
    long timestampShiftUnit = lastTimestamp - firstTimestamp + (secondTimestamp - firstTimestamp);
    for (int i = 2; i < copyNum + 1; i++) {
      System.out.println("copy " + i);
      long timestampShift = timestampShiftUnit * i;
      BufferedReader reader = new BufferedReader(new FileReader(file));
      reader.readLine(); // skip header
      while ((line = reader.readLine()) != null) {
        String[] items = line.split(csvSplitBy);
        long timestamp = Long.parseLong(items[0]) + timestampShift;
        String newLine = timestamp + line.substring(line.indexOf(csvSplitBy));
        writer.println(newLine);
      }
      reader.close();
    }
    writer.close();
    System.out.println("finish copy.");
  }
}