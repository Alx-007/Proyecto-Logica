% Base de conocimientos de enfermedades y síntomas en Prolog

% Definición de enfermedades y síntomas
sintoma(gripe, [fiebre, tos, dolor_cuerpo, congestion]).
sintoma(resfriado, [tos, estornudos, congestion, dolor_garganta]).
sintoma(neumonia, [fiebre, tos, dificultad_respiratoria, dolor_pecho]).
sintoma(bronquitis, [tos, dolor_pecho, fatiga, flema]).
sintoma(covid19, [fiebre, tos_seca, cansancio, perdida_olfato]).
sintoma(influenza, [fiebre_alta, dolor_cuerpo, fatiga, tos]).
sintoma(amigdalitis, [dolor_garganta, fiebre, dolor_cabeza, inflamacion_garganta]).
sintoma(asma, [dificultad_respiratoria, sibilancias, opresion_pecho, tos]).
sintoma(migrana, [dolor_cabeza, sensibilidad_luz, nausea, vision_borrosa]).
sintoma(hepatitis, [fatiga, ictericia, dolor_abdominal, perdida_apetito]).

% Definición de tratamientos
tratamiento(gripe, [reposo, hidratacion, medicamentos_antipireticos]).
tratamiento(resfriado, [reposo, hidratacion, miel, inhalaciones]).
tratamiento(neumonia, [antibioticos, reposo, oxigenoterapia, hidratacion]).
tratamiento(bronquitis, [broncodilatadores, hidratacion, reposo, expectorantes]).
tratamiento(covid19, [aislamiento, medicamentos_antitermicos, reposo, oxigeno]).
tratamiento(influenza, [reposo, medicamentos_antivirales, hidratacion]).
tratamiento(amigdalitis, [antibioticos, analgesicos, reposo, hidratacion]).
tratamiento(asma, [inhaladores, broncodilatadores, evitar_alergenos]).
tratamiento(migrana, [analgesicos, descanso, evitar_estimulantes, oscuridad]).
tratamiento(hepatitis, [reposo, dieta_baja_grasas, evitar_alcohol]).

% Diagnóstico basado en coincidencia de síntomas
diagnosticar(SintomasPaciente, Enfermedad) :-
    sintoma(Enfermedad, SintomasEnfermedad),
    subset(SintomasPaciente, SintomasEnfermedad).

% Tratamiento basado en diagnóstico
obtener_tratamiento(Enfermedad,Tratamiento) :-
    tratamiento(Enfermedad,Tratamiento).