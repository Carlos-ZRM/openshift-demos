{{/*
Expand the name of the chart.
*/}}
{{- define "buildah-from-git.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "buildah-from-git.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "buildah-from-git.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "buildah-from-git.labels" -}}
helm.sh/chart: {{ include "buildah-from-git.chart" . }}
{{ include "buildah-from-git.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "buildah-from-git.selectorLabels" -}}
app.kubernetes.io/name: {{ include "buildah-from-git.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "buildah-from-git.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "buildah-from-git.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}




{{/*
Define fullImageTag:
- If .Values.repository.imageName exists and is not empty, use its value.
- Else, generate a random 8-char string and append the chart version.
*/}}
{{- define "buildah-from-git.fullImageTag" -}}
{{- if and .Values.repository.tag (ne .Values.repository.tag "") -}}
{{ .Values.repository.tag }}
{{- else -}}
{{- $rand := randAlphaNum 8 -}}
{{ printf "%s-%s" $rand .Chart.Version | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}


{{- define "buildah-from-git.fullImageName" -}}
{{- if and .Values.repository.imageName (ne .Values.repository.imageName "") -}}
{{ .Values.repository.imageName }}
{{- else -}}
{{ printf "$" include "buildah-from-git.fullname" . }}
{{- end }}
{{- end }}

{{- define "buildah-from-git.fullRegistryUrl"  -}}

{{- if and .Values.repository.registryUrl (ne .Values.repository.registryUrl "") -}}
{{ printf "$/$/" ( .Values.repository.registryUrl ) ( .Release.Namespace ) }}
{{- else -}}
{{ "image-registry.openshift-image-registry.svc:5000" }}
{{- end }}
{{- end }}

{{- define "buildah-from-git.fullRegistry" -}}
{{ printf "image-registry.openshift-image-registry.svc:5000/%s/%s:latest" ( .Release.Namespace ) ( .Release.Name )  }}
{{- end }}

