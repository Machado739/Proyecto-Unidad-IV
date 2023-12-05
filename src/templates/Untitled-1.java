import javax.swing.*;
import javax.swing.plaf.metal.MetalLookAndFeel;
import javax.swing.plaf.metal.OceanTheme;
import javax.swing.text.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.util.ArrayList;
import java.util.List;

class Editor extends JFrame implements ActionListener {
    JTextPane codePane, errorPane;
    JFrame f;

    Editor() {
        f = new JFrame("Editor");

        try {
            UIManager.setLookAndFeel("javax.swing.plaf.metal.MetalLookAndFeel");
            MetalLookAndFeel.setCurrentTheme(new OceanTheme());
        } catch (Exception e) {
        }

        // Panel para el código
        codePane = new JTextPane();
        codePane.setContentType("text/html");

        // Configurar estilos
        StyledDocument codeDoc = codePane.getStyledDocument();
    Style styleGreen = codeDoc.addStyle("GreenStyle", null);
    StyleConstants.setForeground(styleGreen, Color.GREEN);

    Style styleBlue = codeDoc.addStyle("BlueStyle", null);
    StyleConstants.setForeground(styleBlue, Color.BLUE);

    Style styleRed = codeDoc.addStyle("RedStyle", null);
    StyleConstants.setForeground(styleRed, Color.RED);

    // Nuevo estilo para "again"
    Style styleOrange = codeDoc.addStyle("OrangeStyle", null);
    StyleConstants.setForeground(styleOrange, Color.ORANGE);

        // Configurar el filtro de documento para el área de código
        ((AbstractDocument) codePane.getDocument()).setDocumentFilter(new MyDocumentFilter());

        // Panel para mostrar errores
        errorPane = new JTextPane();
        errorPane.setEditable(false); // Para que el usuario no pueda editar el área de errores

        // Paneles apilados verticalmente
        JPanel panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        panel.add(new JScrollPane(codePane));
        panel.add(new JScrollPane(errorPane));

        f.add(panel);
        f.setSize(800, 600);
        f.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JMenuBar mb = new JMenuBar();
        JMenu m1 = new JMenu("Archivo");
        JMenuItem mi1 = new JMenuItem("Nuevo");
        JMenuItem mi2 = new JMenuItem("Abrir");
        JMenuItem mi3 = new JMenuItem("Guardar");
        JMenuItem mi9 = new JMenuItem("Imprimir");
        mi1.addActionListener(this);
        mi2.addActionListener(this);
        mi3.addActionListener(this);
        mi9.addActionListener(this);
        m1.add(mi1);
        m1.add(mi2);
        m1.add(mi3);
        m1.add(mi9);

        JMenu m2 = new JMenu("Editar");
        JMenuItem mi4 = new JMenuItem("Cortar");
        JMenuItem mi5 = new JMenuItem("Copiar");
        JMenuItem mi6 = new JMenuItem("Pegar");
        JMenuItem mi7 = new JMenuItem("Ejecutar");
        mi4.addActionListener(this);
        mi5.addActionListener(this);
        mi6.addActionListener(this);
        mi7.addActionListener(this);
        m2.add(mi4);
        m2.add(mi5);
        m2.add(mi6);
        m2.add(mi7);

        JMenu m3 = new JMenu("Ayuda");
        JMenuItem mi8 = new JMenuItem("Acerca de");
        mi8.addActionListener(this);
        m3.add(mi8);

        JMenuItem mc = new JMenuItem("Cerrar");
        mc.addActionListener(this);

        mb.add(m1);
        mb.add(m2);
        mb.add(m3);
        mb.add(mc);

        f.setJMenuBar(mb);
        f.setVisible(true);
    }

    // Clase interna para el filtro de documento
    private class MyDocumentFilter extends DocumentFilter {
        @Override
        public void insertString(FilterBypass fb, int offset, String string, AttributeSet attr)
                throws BadLocationException {
            super.insertString(fb, offset, string, attr);
            applyStyles();
        }

        @Override
        public void remove(FilterBypass fb, int offset, int length) throws BadLocationException {
            super.remove(fb, offset, length);
            applyStyles();
        }

        @Override
        public void replace(FilterBypass fb, int offset, int length, String text, AttributeSet attrs)
                throws BadLocationException {
            super.replace(fb, offset, length, text, attrs);
            applyStyles();
        }
    }

   private void applyStyles() {
    SwingUtilities.invokeLater(this::extracted);
    SwingUtilities.invokeLater(() -> {
        StyledDocument doc = codePane.getStyledDocument();
        String text;
        try {
            text = doc.getText(0, doc.getLength());

            // Reiniciar estilo verde después de cada ocurrencia de "Inicio#"
            int indexInicio = text.indexOf("Inicio#");
            while (indexInicio != -1) {
                int start = indexInicio;
                int end = indexInicio + "Inicio#".length();
                doc.setCharacterAttributes(start, end - start, doc.getStyle("GreenStyle"), true);
                indexInicio = text.indexOf("Inicio#", end);
            }

            // Reiniciar estilo azul después de cada ocurrencia de "Out#"
            int indexOut = text.indexOf("Out#");
            while (indexOut != -1) {
                int start = indexOut;
                int end = indexOut + "Out#".length();
                doc.setCharacterAttributes(start, end - start, doc.getStyle("BlueStyle"), true);
                indexOut = text.indexOf("Out#", end);
            }

            // Reiniciar estilo rojo para la palabra "Mensaje"
            int indexMensaje = text.indexOf("Mensaje");
            while (indexMensaje != -1) {
                int start = indexMensaje;
                int end = start + "Mensaje".length();
                doc.setCharacterAttributes(start, end - start, doc.getStyle("RedStyle"), true);
                indexMensaje = text.indexOf("Mensaje", end);
            }

            // Aplicar estilo naranja después de cada ocurrencia de "again"
            int indexAgain = text.indexOf("again");
            while (indexAgain != -1) {
                int start = indexAgain;
                int end = indexAgain + "again".length();
                doc.setCharacterAttributes(start, end - start, doc.getStyle("OrangeStyle"), true);
                indexAgain = text.indexOf("again", end);
            }

        } catch (BadLocationException e) {
            e.printStackTrace();
        }
    });
}

    private void extracted() {
        StyledDocument doc = codePane.getStyledDocument();
        String text;
        try {
            text = doc.getText(0, doc.getLength());

            // Reiniciar estilo verde después de cada ocurrencia de "G#"
            int index = text.indexOf("G#");
            while (index != -1) {
                int start = index + 2; // Posición después de "G#"
                int end = text.indexOf("##", start);
                if (end == -1) {
                    end = text.length();
                }
                doc.setCharacterAttributes(start, end - start, doc.getStyle("GreenStyle"), true);
                index = text.indexOf("G#", end);
            }
            // Reiniciar estilo azul después de cada ocurrencia de "B#"
            index = text.indexOf("B#");
            while (index != -1) {
                int start = index + 2; // Posición después de "B#"
                int end = text.indexOf("##", start);
                if (end == -1) {
                    end = text.length();
                }
                doc.setCharacterAttributes(start, end - start, doc.getStyle("BlueStyle"), true);
                index = text.indexOf("B#", end);
            }
            // Reiniciar estilo rojo después de cada ocurrencia de "R#"
            index = text.indexOf("R#");
            while (index != -1) {
                int start = index + 2; // Posición después de "R#"
                int end = text.indexOf("##", start);
                if (end == -1) {
                    end = text.length();
                }
                doc.setCharacterAttributes(start, end - start, doc.getStyle("RedStyle"), true);
                index = text.indexOf("R#", end);
            }

        } catch (BadLocationException e) {
            e.printStackTrace();
        }
    }

    public void actionPerformed(ActionEvent e) {
        String s = e.getActionCommand();

        if (s.equals("Cortar")) {
            codePane.cut();
        } else if (s.equals("Copiar")) {
            codePane.copy();
        } else if (s.equals("Pegar")) {
            codePane.paste();
        } else if (s.equals("Guardar")) {
            JFileChooser j = new JFileChooser("f:");
            int r = j.showSaveDialog(null);

            if (r == JFileChooser.APPROVE_OPTION) {
                File fi = new File(j.getSelectedFile().getAbsolutePath());

                try {
                    FileWriter wr = new FileWriter(fi, false);
                    BufferedWriter w = new BufferedWriter(wr);
                    w.write(codePane.getText());
                    w.flush();
                    w.close();
                } catch (Exception evt) {
                    JOptionPane.showMessageDialog(f, evt.getMessage());
                }
            } else {
                JOptionPane.showMessageDialog(f, "El usuario canceló la operación");
            }
        } else if (s.equals("Imprimir")) {
            try {
                codePane.print();
            } catch (Exception evt) {
                JOptionPane.showMessageDialog(f, evt.getMessage());
            }
        } else if (s.equals("Abrir")) {
            JFileChooser j = new JFileChooser("f:");
            int r = j.showOpenDialog(null);

            if (r == JFileChooser.APPROVE_OPTION) {
                File fi = new File(j.getSelectedFile().getAbsolutePath());

                try {
                    String s1 = "", sl = "";
                    FileReader fr = new FileReader(fi);
                    BufferedReader br = new BufferedReader(fr);
                    sl = br.readLine();

                    while ((s1 = br.readLine()) != null) {
                        sl = sl + "\n" + s1;
                    }

                    codePane.setText(sl);
                } catch (Exception evt) {
                    JOptionPane.showMessageDialog(f, evt.getMessage());
                }
            } else {
                JOptionPane.showMessageDialog(f, "El usuario canceló la operación");
            }
        } else if (s.equals("Nuevo")) {
            codePane.setText("");
        } else if (s.equals("Cerrar")) {
            f.setVisible(false);
        } else if (s.equals("Acerca de")) {
            JOptionPane.showMessageDialog(f, "Este es un editor de texto simple creado en Java.");
        } else if (s.equals("Ejecutar")) {
            // Obtener el texto del JTextPane
            String texto = codePane.getText();

            // Validar el texto
            if (validarTexto(texto)) {

            } else {
                mostrarErrores();
            }
        }

        applyStyles(); // Aplicar estilos después de cada acción
    }

    private List<String> errores = new ArrayList<>();

    private boolean validarTexto(String texto) {
        errores.clear(); // Limpiar la lista de errores antes de validar cada vez
        errorPane.setText(""); // Limpiar el área de errores

        // Obtener el contenido visible del JTextPane
        String textoVisible = obtenerTextoVisible();

        // Contador de ocurrencias de "again"
        int contadorAgain = 0;

        // Verificar que el texto comienza con "Inicio#" y termina con "Out#"
        if (textoVisible.startsWith("Inicio#") && textoVisible.endsWith("Out#")) {
            // Buscar la estructura "again(x)#" donde x es el número de repeticiones
            int startAgain = textoVisible.indexOf("again(");
            if (startAgain != -1) {
                int endAgain = textoVisible.indexOf(")", startAgain);
                if (endAgain != -1) {
                    // Obtener el contenido entre paréntesis
                    String contenidoEntreParentesis = textoVisible.substring(startAgain + "again(".length(), endAgain).trim();

                    try {
                        // Obtener el número de repeticiones como entero
                        int repeticiones = Integer.parseInt(contenidoEntreParentesis);

                        // Verificar si el contenido está entre comillas
                        if (repeticiones > 0) {
                            // Obtener el mensaje entre comillas
                            int startMensaje = textoVisible.indexOf("Mensaje(\"");
                            int endMensaje = textoVisible.indexOf("\")", startMensaje);
                            if (startMensaje != -1 && endMensaje != -1) {
                                String mensaje = textoVisible.substring(startMensaje + "Mensaje(\"".length(), endMensaje);

                                // Imprimir el mensaje varias veces según el número de repeticiones
                                for (int i = 0; i < repeticiones; i++) {
                                    JOptionPane.showMessageDialog(f, mensaje);
                                }

                                // Actualizar el contador de ocurrencias de "again"
                                contadorAgain += repeticiones;
                            } else {
                                agregarError("Falta el mensaje entre comillas.");
                            }
                        } else {
                            agregarError("El número de repeticiones debe ser mayor que 0.");
                        }
                    } catch (NumberFormatException e) {
                        agregarError("El contenido entre paréntesis no es un número válido.");
                    }
                } else {
                    agregarError("Falta ')' después de 'again('.");
                }
            } else {
                // Si no hay estructura "again(x)#", imprimir el mensaje una vez
                int startMensaje = textoVisible.indexOf("Mensaje(\"");
                int endMensaje = textoVisible.indexOf("\")", startMensaje);
                if (startMensaje != -1 && endMensaje != -1) {
                    String mensaje = textoVisible.substring(startMensaje + "Mensaje(\"".length(), endMensaje);
                    JOptionPane.showMessageDialog(f, mensaje);
                }
            }
        }

        // Mostrar el número de ocurrencias de "again"
        System.out.println("Número de veces que dice 'again': " + contadorAgain);

        // Mostrar los errores si los hay
        if (!errores.isEmpty()) {
            mostrarErrores();
            return false;
        }

        return true;
    }

    private int contarOcurrencias(String texto, String palabra) {
        int contador = 0;
        int index = texto.indexOf(palabra);
        while (index != -1) {
            contador++;
            index = texto.indexOf(palabra, index + 1);
        }
        return contador;
    }

    private void agregarError(String mensaje) {
        // Agregar mensaje de error al área de errores
        errorPane.setText(errorPane.getText() + mensaje + "\n");
    }

    private void mostrarErrores() {
        if (!errores.isEmpty()) {
            StringBuilder mensajeError = new StringBuilder("Se encontraron los siguientes errores:\n");
            for (String error : errores) {
                mensajeError.append("- ").append(error).append("\n");
            }
            JOptionPane.showMessageDialog(f, mensajeError.toString());
        }
    }




private String obtenerTextoVisible() {
    // Obtener el contenido del JTextPane sin formato adicional
    Document doc = codePane.getDocument();
    int start = doc.getStartPosition().getOffset();
    int end = doc.getEndPosition().getOffset();
    try {
        return doc.getText(start, end - start).trim();
    } catch (BadLocationException e) {
        e.printStackTrace();
    }
    return "";
}



    // Método main y otras partes del código permanecen sin cambios
   public static void main(String args[]) {
        Editor e = new Editor();
    }
}
