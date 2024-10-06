
        importCpg("/home/murilodepa/Documents/master/API_Usage_Patterns_Extractor/projects/Experiments-of-Operational-System-A/Tarefa1.c.cpg.bin")
        val edges = cpg.call
        .filterNot(_.name.startsWith("<operator>")) // Ignore operators if necessary
        .map { call =>
        val caller = call.method.fullName       // Full name of the calling function
        val callee = call.name                  // Name of the called function
        (caller, callee)                        // Return the tuple (caller, callee)
        }.l

        // Print each edge in the call graph
        edges.foreach { case (caller, callee) =>
        println(s"Caller: $caller -> Callee: $callee")  
        }
        