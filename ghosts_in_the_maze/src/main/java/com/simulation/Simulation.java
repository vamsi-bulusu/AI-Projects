package com.simulation;

import com.environment.classes.Environment;
import org.apache.poi.ss.usermodel.*;
import java.io.*;
import java.nio.file.Path;
import java.nio.file.Paths;


public class Simulation {

    public static final String path = getPath() + "/util/";

    public static String getPath(){
        Path currentRelativePath = Paths.get("");
        return currentRelativePath.toAbsolutePath().toString();
    }
    public static File createTextFile(String filename){
        File file = new File(filename);
        try {
            if (file.createNewFile()) {
                System.out.println("New Metrics File is created!");
            } else {
                System.out.println("File already exists.");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return file;
    }

    public static void writeToFile(Environment environment, String filename, int success, int totalSim) throws IOException {
        File file = createTextFile(path + filename);
        FileWriter writer = new FileWriter(file, true);
        int numGhosts = environment.ghosts.size();
        writer.write("SUCCESS: " + success + " GHOST: " + numGhosts + "TOTAL: " + totalSim + "\n" + environment + "\n");
        writer.close();
    }

    public static void insertRow(Object[] objectArr,Sheet sheet, int rowId){
        Row row = sheet.createRow(rowId);
        int cellId = 0;
        for (Object obj : objectArr) {
            Cell cell = row.createCell(cellId++);
            cell.setCellValue(obj.toString());
        }
    }
    public static void writeToExcel(Environment environment, String filename, int success, int totalSim) {
        try {
            File file = new File(path + filename);
            Workbook workbook = file.exists() ? WorkbookFactory.create(new FileInputStream(file)) : WorkbookFactory.create(file.createNewFile());
            Sheet sheet = workbook.getSheet(filename);
            if(sheet == null) sheet = workbook.createSheet(filename);
            Object[] objects;
            int rowId = sheet.getLastRowNum();
            System.out.println("RowId: " + rowId);
            if(rowId == -1){
                objects = new Object[] {"Ghosts", "Success", "Simulations"};
                insertRow(objects, sheet, ++rowId);
            }

            insertRow(new Object[]{String.valueOf(environment.ghosts.size()), String.valueOf(success), String.valueOf(totalSim)}, sheet, ++rowId);
            FileOutputStream out = new FileOutputStream(path + filename);
            workbook.write(out);
            out.close();
            workbook.close();
        }
        catch (IOException e){
            System.out.println("An error occurred");
            e.printStackTrace();
        }

    }
}
