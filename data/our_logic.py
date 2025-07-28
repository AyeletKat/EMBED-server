# route: /filter/options
# changes to do in the server side: return the unique values for our filtersn   ♠
# changes to do in the electron side: ---------------

# route: /filter/abnormality-options
# changes to do in the server side: return the unique values for our abnormality filtersn   ♠
# changes to do in the electron side: ---------------

# route: /filter/patients-ids
# changes to do in the server side: delete it - we do not work with patient_ids   ♠
# changes to do in the electron side: ---------------


# route: /patients/ TODO understand what this route returns
# changes to do in the server side: make it return our metadata, adjust the existing function *in progress*
# changes to do in the electron side: ??

# route: /patients/patient_id
# changes to do in the server side: delete it ?? if its really only used for the patient_id filters then we don't need it,
# changes to do in the electron side: maybe delete the channel that use it ?

# route: /patients/filter
# changes to do in the server side: make it return the empi_anon, acc_anon and side of the images that match the filters
# changes to do in the electron side: make it receive all the four parameters and send them to image/ route


# route: /<patient_id>/images-metadata
# changes to do in the server side: make it return the image metadata by empi_anon, acc_anon and side and not by patient_id
# changes to do in the electron side: make it send the empi_anon, acc_anon and side to the server and not the patient_id

# route: /<patient_id>/full
# changes to do in the server side: make it return the image by getting its path by the empi_anon, acc_anon and side and not by patient_id
# changes to do in the electron side: make it send the empi_anon, acc_anon and side to the server and not the patient_id